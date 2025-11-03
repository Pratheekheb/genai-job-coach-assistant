from fastapi import APIRouter,Request,UploadFile,Form
from typing import Optional
from pydantic import BaseModel
from llm_handler import run_prompt
import io
from PyPDF2 import PdfReader
from docx import Document 
from template import CAREER_ADVICE_PROMPT,INTERVIEW_QUESTIONS_PROMPT,RESUME_TIPS_PROMPT
router=APIRouter()
class generateRequest(BaseModel):
    role:str
    tone:str
    choice:int
    
@router.post("/generate")
async def generate(
    request:Request,
    role:str=Form(...),
    tone:str=Form(...),
    choice:int=Form(...),
    resume:Optional[UploadFile]=None

):
    if not resume:    
        try:
            json_data=await request.json()
            data=generateRequest(**json_data)
            role,tone,choice=data.role,data.tone,data.choice
        except Exception as e:
            return {"error":f"Invalid JSON input:{e}"}
    resume_text=None
    if resume:
        
        try:
            contents=await resume.read()
            if resume.filename.endswith(".pdf"):
                pdf=PdfReader(io.BytesIO(contents))
                resume_text=" ".join([page.extract_text() or "" for page in pdf.pages])
            elif resume.filename.endswith(".docx"):
                doc=Document(io.BytesIO(contents))
                resume_text=" ".join([p.text for p in doc.paragraphs])
            else:
                return{"error":"Unsupported file format .Please upload a PDF or DOCX file ."}
        except Exception as e:
            return {"error":f"Failed to read resume {e}"}
    if choice==1:
        res=run_prompt(CAREER_ADVICE_PROMPT,persona="career advisor",role=role,tone=tone,resume_text=resume_text)
    elif choice==2:
        res=run_prompt(INTERVIEW_QUESTIONS_PROMPT,role=role,tone=tone,resume_text=resume_text)
    elif choice==3:
        res=run_prompt(RESUME_TIPS_PROMPT,role=role,tone=tone,resume_text=resume_text)
    else:
        return {"error":"Invalid Choice !Must be 1 or 2 or 3."}
    return {
        "result":res if res else "Error:Model output couldnt be parsed or validated .",
        "resume_preview":resume_text[:800] if resume_text else None
        } 