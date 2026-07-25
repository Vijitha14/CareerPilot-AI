from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.services.ats_service import analyze_ats

from backend.services.parser_service import (
    extract_text_from_pdf,
    extract_sections,
    calculate_word_count,
)

from backend.services.evidence_service import analyze_candidate_evidence

from backend.services.groq_service import (
    analyze_career_fit,
    analyze_job_fit,
    analyze_resume_improvements,
)

from backend.services.job_service import build_job_context


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="CareerPilot AI API",
    description="Backend API for CareerPilot AI resume intelligence.",
    version="1.0.0",
)


# =========================================================
# CORS
# =========================================================

# Allows the Streamlit frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# ROOT ROUTE
# =========================================================

@app.get("/")
def root():
    return {
        "message": "CareerPilot AI backend is running ✈️"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# =========================================================
# RESUME ANALYSIS
# =========================================================

@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(default="")
):

    # -----------------------------------------------------
    # Validate resume
    # -----------------------------------------------------

    if not resume.filename:
        raise HTTPException(
            status_code=400,
            detail="Resume filename is missing."
        )

    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Currently only PDF resumes are supported."
        )

    try:

        # -------------------------------------------------
        # 1. Extract resume text
        # -------------------------------------------------

        raw_text = extract_text_from_pdf(
            resume.file
        )

        if not raw_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from this resume."
            )


        # -------------------------------------------------
        # 2. Extract resume sections
        # -------------------------------------------------

        sections = extract_sections(
            raw_text
        )

        word_count = calculate_word_count(
            raw_text
        )


        # -------------------------------------------------
        # 3. Build parsed resume
        # -------------------------------------------------

        parsed_resume = {
            "raw_text": raw_text,
            "sections": sections,
            "word_count": word_count,
        }


        # -------------------------------------------------
        # 4. Build candidate evidence
        # -------------------------------------------------

        candidate_evidence = analyze_candidate_evidence(
            parsed_resume
        )
        # ---------- ATS analysis ----------
        ats_analysis = analyze_ats(
            parsed_resume,
            candidate_evidence
        )
        # ---------- Resume improvements ----------
        resume_improvements = analyze_resume_improvements(
            candidate_evidence,
            ats_analysis
        )


        # -------------------------------------------------
        # 5. Build job context
        # -------------------------------------------------

        job_context = build_job_context(
            job_description
        )


        # -------------------------------------------------
        # 6. Choose CareerPilot analysis mode
        # -------------------------------------------------

        if job_description.strip():

            # =============================================
            # MODE 1: JOB FIT ANALYSIS
            # =============================================

            analysis_mode = "job_fit"

            career_analysis = analyze_job_fit(
                candidate_evidence,
                job_context
            )

        else:

            # =============================================
            # MODE 2: CAREER DISCOVERY
            # =============================================

            analysis_mode = "career_discovery"

            career_analysis = analyze_career_fit(
                candidate_evidence
            )


        # -------------------------------------------------
        # 7. Return final analysis
        # -------------------------------------------------

        return {
            "filename": resume.filename,

            "word_count": word_count,

            "sections_found": list(
                sections.keys()
            ),

            "analysis_mode": analysis_mode,

            "job_description_provided": bool(
                job_description.strip()
            ),

            "candidate_evidence": candidate_evidence,

            "job_context": job_context,

            "career_analysis": career_analysis,
            "ats_analysis": ats_analysis,
            "resume_improvements": resume_improvements,
        }


    # -----------------------------------------------------
    # Keep FastAPI errors intact
    # -----------------------------------------------------

    except HTTPException:
        raise


    # -----------------------------------------------------
    # Handle unexpected errors
    # -----------------------------------------------------

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Resume analysis failed: {str(error)}"
        )