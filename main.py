from fastapi import FastAPI, HTTPException
import os
import random
from schemas.model import ResumeAnalysisRequest,VideoAnalysisRequest,AssessmentCheckRequest,AssessmentGenerateRequest
from video_utility.download import download_file
from video_utility.video_analyzer import VideoAnalyzer
from ats_utility.resume_analyzer import ResumeExtractor,analyze_resume

from assesment_utlity.assesment_generate import question_answer




app =FastAPI()

@app.post("/analyze-resume")
async def analyze_resume_endpoint(request: ResumeAnalysisRequest):
    """
    Analyze resume from URL against job description
    """
    try:
        # Download resume file
        file_extension = os.path.splitext(str(request.resume_url))[-1].lower()
        temp_file_path = await download_file(str(request.resume_url), file_extension)

        # Read file content
        with open(temp_file_path, 'rb') as f:
            file_content = f.read()

        # Extract text based on file type
        if file_extension == '.pdf':
            resume_text = await ResumeExtractor.extract_from_pdf(file_content)
        elif file_extension == '.docx':
            resume_text = await ResumeExtractor.extract_from_docx(file_content)
        elif file_extension == '.txt':
            resume_text = await ResumeExtractor.extract_from_txt(file_content)
        elif file_extension in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
            resume_text = await ResumeExtractor.extract_from_image(file_content)
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format"
            )

        # Analyze resume
        print("------text------------",resume_text, request.job_description)
        analysis = await analyze_resume(resume_text, request.job_description)

        # Cleanup
        os.unlink(temp_file_path)

        return {
            "status": "success",
            "data": analysis
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/analyze-video")
async def analyze_video_endpoint(request: VideoAnalysisRequest):
    """
    Analyze video interview from URL
    """
    try:
        # Download video and reference face image
        video_path = await download_file(str(request.video_url), '.mp4')
        face_path = await download_file(str(request.reference_face_url), '.jpg')

        # Initialize analyzer and process video
        analyzer = VideoAnalyzer(face_path)
        analysis_results = analyzer.analyze(video_path)

        # Cleanup
        os.unlink(video_path)
        os.unlink(face_path)

        return {
            "status": "success",
            "data": analysis_results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-assessment")
async def generate_assessment(request: AssessmentGenerateRequest):
    assessment =question_answer(job_description=request.job_description,num_questions=request.num_questions,question_type=request.question_type,question_traits=request.question_traits,question_level=request.question_level)
    
    return {
        "status": "success",
       "data": assessment
    }
from assesment_utlity.assesment_checker import mark_evalution
@app.post("/check-assessment")
async def check_assessment(request: AssessmentCheckRequest):
    print("---------------------",request.assessment_content)
    report =mark_evalution(request.assessment_content)
    return {
        "status": "success",
         "data": report
         }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}