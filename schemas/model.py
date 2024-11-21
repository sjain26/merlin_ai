
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict





class ResumeAnalysisRequest(BaseModel):
    resume_url: HttpUrl
    job_description: str

class VideoAnalysisRequest(BaseModel):
    video_url: HttpUrl
    reference_face_url: HttpUrl







class AssessmentGenerateRequest(BaseModel):
    job_description: str
    question_type: str
    num_questions :str
    question_traits:str
    question_level:str

class AssessmentCheckRequest(BaseModel):
    assessment_content: List[Dict]