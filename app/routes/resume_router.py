from fastapi import FastAPI, APIRouter, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path
import logging
import uuid
import os
import aiohttp
import asyncio

from app.models.resume_parser import parse_resume
from app.models.jd_parser import parse_jd
from app.models.summarizer import summarize_resume
from app.models.scorer import score_resume
from app.models.feedback import feed_back

# Initialize router
router = APIRouter(
    prefix="/api",
    tags=["resume"]
)

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Response Models
class ResumeAnalysisResponse(BaseModel):
    summary: str
    score: float
    alignment: float
    feedback: str

class ErrorResponse(BaseModel):
    detail: str

# Configure upload directory
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

def allowed_file(filename: str) -> bool:
    """Check if the file extension is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

async def download_drive_file(drive_link: str) -> Path:
    """Download a file from Google Drive and return the local file path."""
    try:
        # Extract file ID from different Google Drive link formats
        if "id=" in drive_link:
            file_id = drive_link.split("id=")[1].split("&")[0]
        elif "/d/" in drive_link:
            file_id = drive_link.split("/d/")[1].split("/")[0]
        else:
            raise HTTPException(status_code=400, detail="Invalid Google Drive link format")

        # Google Drive direct download URL
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(download_url) as response:
                if response.status != 200:
                    raise HTTPException(status_code=400, detail="Failed to download file from Google Drive")

                # Generate unique filename
                filename = f"{uuid.uuid4()}.pdf"  # Assuming PDF; adapt based on file type detection
                file_path = UPLOAD_FOLDER / filename

                # Save file
                with open(file_path, "wb") as f:
                    f.write(await response.read())

                logger.debug(f"File downloaded and saved at: {file_path}")
                return file_path

    except Exception as e:
        logger.error(f"Error downloading file from Google Drive: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process Google Drive file: {str(e)}")

async def process_resume(file_path: Path, job_description: str) -> ResumeAnalysisResponse:
    """Process a resume file and return the analysis response."""
    try:
        # Parse resume
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
        feedback = feed_back(resume_content, jd_content)

        return ResumeAnalysisResponse(
            summary=summary,
            score=score,
           alignment=alignment,
            feedback=feedback
        )

    except Exception as e:
        logger.error(f"Error processing resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Resume processing failed: {str(e)}")

    finally:
        # Clean up temporary file
        if file_path.exists():
            try:
                os.remove(file_path)
            except Exception as e:
                logger.warning(f"Could not delete temporary file: {str(e)}")

@router.post(
    "/analyze-resumes",
    response_model=List[ResumeAnalysisResponse],
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}
)
async def analyze_resumes(
    job_description: str = Form(...),
    drive_links: List[str] = Form(...)
):
    """
    Analyze multiple resumes from Google Drive links against a job description.

    Parameters:
    - job_description: Job description text
    - drive_links: List of Google Drive links for resumes

    Returns:
    - List of resume analysis responses
    """
    logger.debug(f"Received {len(drive_links)} resumes for analysis.")

    if not drive_links:
        raise HTTPException(status_code=400, detail="No resume links provided")

    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required")

    # Download and process resumes in parallel
    file_tasks = [download_drive_file(link) for link in drive_links]
    file_paths = await asyncio.gather(*file_tasks, return_exceptions=True)

    # Filter out failed downloads
    valid_file_paths = [path for path in file_paths if isinstance(path, Path)]
    if not valid_file_paths:
        raise HTTPException(status_code=400, detail="No valid resumes downloaded")

    # Process resumes in parallel
    analysis_tasks = [process_resume(file, job_description) for file in valid_file_paths]
    results = await asyncio.gather(*analysis_tasks, return_exceptions=True)

    # Filter out failed analyses
    successful_results = [result for result in results if isinstance(result, ResumeAnalysisResponse)]

    if not successful_results:
        raise HTTPException(status_code=500, detail="Failed to process all resumes")

    return successful_results

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}
