from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from ..models.extract_doc import process_input
from ..openai.llm import LLMClient
import os
from pathlib import Path

question_bp = APIRouter(
    prefix="/questions",
    tags=["questions"]
)

UPLOAD_FOLDER = Path("uploads")
ALLOWED_EXTENSIONS = {'pdf', 'txt'}

if not UPLOAD_FOLDER.exists():
    UPLOAD_FOLDER.mkdir(parents=True)

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@question_bp.post("/generate")
async def generate_questions(
    file: UploadFile = File(None),
    text: str = Form(None)
):
    try:
        if not file and not text:
            raise HTTPException(status_code=400, detail="No file or text provided")

        content_text = ""
        
        if file:
            if not allowed_file(file.filename):
                raise HTTPException(status_code=400, detail="Invalid file type")
            
            filepath = UPLOAD_FOLDER / file.filename
            
            # Save uploaded file
            with open(filepath, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            try:
                content_text = process_input(str(filepath))
            finally:
                # Clean up
                if filepath.exists():
                    os.remove(filepath)
        else:
            content_text = text

        if not content_text:
            raise HTTPException(status_code=400, detail="Failed to extract content")

        # Get the instruction from question_generator
        with open('app/routes/question_generator.py', 'r') as f:
            instruction = f.read().split('instruction="""')[1].split('"""')[0]

        # Combine instruction with content
        prompt = f"{instruction}\n\nContent to analyze:\n{content_text}"

        # Generate questions using LLM
        llm_client = LLMClient()
        response = llm_client.generate_response(prompt)

        if 'error' in response:
            raise HTTPException(status_code=500, detail=response['error'])

        return JSONResponse(content=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))