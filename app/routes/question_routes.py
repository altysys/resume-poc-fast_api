from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from ..models.extract_doc import process_input
from ..models.mcq_generator import MCQGenerator
import os
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

mcq_bp = APIRouter(
    prefix="/questions",
    tags=["questions"]
)

UPLOAD_FOLDER = Path("uploads")
ALLOWED_EXTENSIONS = {'pdf', 'txt'}

if not UPLOAD_FOLDER.exists():
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@mcq_bp.post("/generate")
async def generate_questions(
    file: UploadFile = File(None),
    text: str = Form(None)
):
    try:
        if not file and not text:
            raise HTTPException(status_code=400, detail="No file or text provided")

        content_text = ""
        
        if file:
            logger.debug(f"Processing file: {file.filename}")
            if not allowed_file(file.filename):
                raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and TXT files are allowed")
            
            filepath = UPLOAD_FOLDER / file.filename
            logger.debug(f"Saving file to: {filepath}")
            
            # Ensure upload directory exists
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # Save uploaded file
            try:
                content = await file.read()
                with open(filepath, "wb") as buffer:
                    buffer.write(content)
                logger.debug("File saved successfully")
            except Exception as e:
                logger.error(f"Error saving file: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
            
            try:
                content_text = process_input(str(filepath))
                logger.debug("File content extracted successfully")
            except Exception as e:
                logger.error(f"Error processing file: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
            finally:
                # Clean up
                if filepath.exists():
                    try:
                        os.remove(filepath)
                        logger.debug("Temporary file cleaned up")
                    except Exception as e:
                        logger.warning(f"Could not delete temporary file: {str(e)}")
        else:
            content_text = text
            logger.debug("Using provided text content")

        if not content_text:
            raise HTTPException(status_code=400, detail="Failed to extract content")

        # Generate MCQs
        logger.debug("Initializing MCQ generator")
        try:
            mcq_generator = MCQGenerator()
            questions = mcq_generator.generate_mcqs_from_text(content_text)
            logger.debug("MCQs generated successfully")
        except ValueError as ve:
            logger.error(f"Configuration error: {str(ve)}")
            raise HTTPException(
                status_code=500,
                detail="MCQ generation failed: OpenAI API configuration is incomplete. Please check server configuration."
            )

        if 'error' in questions:
            logger.error(f"MCQ generation error: {questions['error']}")
            raise HTTPException(status_code=500, detail=questions['error'])

        return JSONResponse(content=questions)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))