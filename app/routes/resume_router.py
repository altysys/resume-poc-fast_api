# app/routes/resume_router.py
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import logging
import uuid
import os

from app.models.resume_parser import parse_resume
from app.models.jd_parser import parse_jd
from app.models.summarizer import summarize_resume
from app.models.scorer import score_resume
from app.models.question_gen import generate_questions

# Set up logging
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter()

# Configure paths
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
UPLOAD_FOLDER = BASE_DIR / "uploads"

# Create necessary directories
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# Configure templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Allowed file extensions
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

def allowed_file(filename: str) -> bool:
    """Check if the file extension is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Serve the upload form."""
    logger.debug("Accessing index route")
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/upload")
async def upload_resume(
    request: Request,
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """Handle file upload and processing."""
    logger.debug(f"Received upload request for file: {file.filename}")
    
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
        
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file format. Please upload a PDF, DOCX, or TXT file."
        )

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

        return {
            "summary": summary,
            "score": score,
            "alignment": alignment,
            "questions": questions
        }

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