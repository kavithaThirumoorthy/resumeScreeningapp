

from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from app.parsepdf import parse_pdf
from sanjaykapps.resumeScreeningapp.app.agents.cv_extractor_agent import analyze_resume
from sanjaykapps.resumeScreeningapp.app.agents.jobdesc_idenfying_agent import analyze_jd
from sanjaykapps.resumeScreeningapp.app.agents.applicant_analysis_agent import evaluate_candidate
import json

app = FastAPI()

@app.post("/resume_screening/")
async def upload_resume(resume: UploadFile):
    

    resume_text = parse_pdf(resume.file)

    candidate_details = analyze_resume(resume_text)

    jd_text = ""
    with open ("resources/job_description.pdf", "rb") as file:
        jd_text = parse_pdf(file)

    jd_details = analyze_jd(jd_text)

    evaluation = evaluate_candidate(candidate_details, jd_details)

    print("Evaluation result:", evaluation)

    result_json = json.loads(evaluation)
    return JSONResponse(content=result_json)
    
    