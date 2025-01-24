from fastapi import FastAPI, APIRouter, File, UploadFile, Form, HTTPException

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path
import logging
import uuid
import os

from app.models.resume_parser import parse_resume
from app.models.jd_parser import parse_jd
from app.models.summarizer import summarize_resume
from app.models.scorer import score_resume
from app.models.question_gen import generate_questions

# Initialize router
router = APIRouter(
    prefix="/api",
    tags=["resume"]
)


# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Response Models
class ResumeAnalysisResponse(BaseModel):
    summary: str
    score: float
    alignment: float
    questions: List[str]
    
class ErrorResponse(BaseModel):
    detail: str

# Allowed file extensions
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

def allowed_file(filename: str) -> bool:
    """Check if the file extension is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@router.post(
    "/analyze-resume",  # Note: no /api prefix here since we defined it in the router
    response_model=ResumeAnalysisResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
) -> ResumeAnalysisResponse:
    """
    Analyze a resume against a job description.
    
    Parameters:
    - file: Resume file (PDF, DOCX, or TXT)
    - job_description: Job description text
    
    Returns:
    - summary: Resume summary
    - score: Match score between resume and job description
    - alignment: Alignment percentage
    - questions: Generated interview questions
    """
    logger.debug(f"Received analysis request for file: {file.filename}")
    
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
        
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file format. Please upload a PDF, DOCX, or TXT file."
        )
    
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required")

    # Create unique filename
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = UPLOAD_FOLDER / filename

    try:
        # Save the file
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        logger.debug(f"File saved at: {file_path}")

        # Process resume
        resume_content = parse_resume(str(file_path))
        if not resume_content:
            raise HTTPException(status_code=400, detail="No content extracted from resume")
        
        # Process job description
        jd_content = parse_jd(job_description)
        if not jd_content:
            raise HTTPException(status_code=400, detail="No content extracted from job description")
        
        # Generate summary and score
        summary = summarize_resume(resume_content)
        score, alignment = score_resume(summary, jd_content)
        
        # Generate questions if alignment is good enough
        questions = []
        if alignment >= 60:
            questions = generate_questions(resume_content, jd_content)
            
        return ResumeAnalysisResponse(
            summary=summary,
            score=score,
            alignment=alignment,
            questions=questions
        )

    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Clean up the uploaded file
        if file_path.exists():
            try:
                os.remove(file_path)
            except Exception as e:
                logger.warning(f"Could not delete temporary file: {str(e)}")

@router.get("/health")  # Changed from @app.get to @router.get
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

# Configure upload directory
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

