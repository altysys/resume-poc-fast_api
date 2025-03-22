from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from ..models.mcq_generator import MCQGenerator
import os
from pathlib import Path

mcq_bp = APIRouter(
    prefix="/mcq",
    tags=["mcq"]
)

UPLOAD_FOLDER = Path("uploads")
ALLOWED_EXTENSIONS = {'pdf', 'txt'}

if not UPLOAD_FOLDER.exists():
    UPLOAD_FOLDER.mkdir(parents=True)

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@mcq_bp.post("/generate")
async def generate_mcqs(
    file: UploadFile = File(None),
    text: str = Form(None)
):
    try:
        mcq_generator = MCQGenerator()

        if file:
            if not allowed_file(file.filename):
                raise HTTPException(status_code=400, detail="Invalid file type")
            
            filepath = UPLOAD_FOLDER / file.filename
            
            # Save uploaded file
            with open(filepath, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            try:
                result = mcq_generator.generate_mcqs_from_pdf(str(filepath))
            finally:
                # Clean up
                if filepath.exists():
                    os.remove(filepath)
            
            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])
            
            return JSONResponse(content=result)

        elif text:
            result = mcq_generator.generate_mcqs_from_text(text)
            
            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])
            
            return JSONResponse(content=result)

        raise HTTPException(status_code=400, detail="No file or text provided")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))