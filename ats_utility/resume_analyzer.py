from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

from fastapi import FastAPI, HTTPException, UploadFile, Form, File
import openai
from typing import Dict
import PyPDF2
import io
import os
from pydantic import BaseModel
import json
import pytesseract
from PIL import Image
from docx import Document
import fitz  # PyMuPDF for PDF
import asyncio
import aiofiles
from fastapi.middleware.cors import CORSMiddleware
import tempfile

# Load environment variables

os.getenv("OPENAI_API_KEY")
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResumeExtractor:
    """Class to handle different resume formats"""
    
    @staticmethod
    async def extract_from_pdf(file_content: bytes) -> str:
        """Extract text from PDF using PyMuPDF"""
        try:
            with fitz.open(stream=file_content, filetype="pdf") as doc:
                text = ""
                for page in doc:
                    text += page.get_text() + "\n"
                return text.strip()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error extracting PDF text: {str(e)}")

    @staticmethod
    async def extract_from_docx(file_content: bytes) -> str:
        """Extract text from DOCX"""
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
                tmp_file.write(file_content)
                tmp_file.flush()
                
                doc = Document(tmp_file.name)
                text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                
                # Clean up temp file
                os.unlink(tmp_file.name)
                return text.strip()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error extracting DOCX text: {str(e)}")

    @staticmethod
    async def extract_from_image(file_content: bytes) -> str:
        """Extract text from images using OCR"""
        try:
            # Create a temporary file to save the image
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                tmp_file.write(file_content)
                tmp_file.flush()
                
                # Use Tesseract OCR
                text = pytesseract.image_to_string(Image.open(tmp_file.name))
                
                # Clean up temp file
                os.unlink(tmp_file.name)
                return text.strip()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error extracting text from image: {str(e)}")

    @staticmethod
    async def extract_from_txt(file_content: bytes) -> str:
        """Extract text from TXT file"""
        try:
            return file_content.decode('utf-8').strip()
        except UnicodeDecodeError:
            try:
                # Try different encodings if UTF-8 fails
                encodings = ['latin-1', 'iso-8859-1', 'cp1252']
                for encoding in encodings:
                    try:
                        return file_content.decode(encoding).strip()
                    except UnicodeDecodeError:
                        continue
                raise HTTPException(status_code=400, detail="Unable to decode text file with supported encodings")
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error extracting text from TXT: {str(e)}")

async def analyze_resume(resume_text: str, job_description: str) -> Dict:
    """Analyze resume against job description using OpenAI API"""
    try:
        client = openai.Client()
        
        prompt = f"""
        Analyze this resume against the job description and provide:
        1. An overall match score (0-100)
        2. Key skills found in both resume and job description
        3. Missing key skills from job description
        4. Specific recommendations for improvement
        5. Experience level match
        6. Education match
        
        Resume:
        {resume_text}
        
        Job Description:
        {job_description}
        
        Return response as JSON with this structure:
        {{
            "match_score": number,
            "matched_skills": [string],
            "missing_skills": [string],
            "recommendations": [string],
            "experience_match": {{
                "required": string,
                "actual": string,
                "matches": boolean
            }},
            "education_match": {{
                "required": string,
                "actual": string,
                "matches": boolean
            }}
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an expert ATS system and resume analyzer."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")

@app.post("/analyze-resume")
async def analyze_resume_endpoint(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Endpoint to analyze resume against job description
    Supports multiple file formats: PDF, DOCX, TXT, and common image formats
    
    Parameters:
    - resume: File (PDF/DOCX/TXT/IMAGE)
    - job_description: Text of the job description
    
    Returns:
    - Detailed analysis including match score, skills, recommendations, etc.
    """
    try:
        # Read file content
        file_content = await resume.read()
        
        # Get file extension
        file_ext = os.path.splitext(resume.filename)[1].lower()
        
        # Extract text based on file type
        if file_ext == '.pdf':
            resume_text = await ResumeExtractor.extract_from_pdf(file_content)
        elif file_ext == '.docx':
            resume_text = await ResumeExtractor.extract_from_docx(file_content)
        elif file_ext == '.txt':
            resume_text = await ResumeExtractor.extract_from_txt(file_content)
        elif file_ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
            resume_text = await ResumeExtractor.extract_from_image(file_content)
        else:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file format. Supported formats: PDF, DOCX, TXT, PNG, JPG, JPEG, TIFF, BMP"
            )
        
        # Analyze resume
        analysis = await analyze_resume(resume_text, job_description)
        
        return {
            "status": "success",
            "data": {
                "match_score": analysis["match_score"],
                "matched_skills": analysis["matched_skills"],
                "missing_skills": analysis["missing_skills"],
                "recommendations": analysis["recommendations"],
                "experience_match": analysis["experience_match"],
                "education_match": analysis["education_match"]
            }
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}