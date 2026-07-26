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
    generate_gap_action_plan,
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# ROOT
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

        # =================================================
        # 1. EXTRACT RESUME TEXT
        # =================================================

        raw_text = extract_text_from_pdf(
            resume.file
        )

        if not raw_text or not raw_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from this resume."
            )


        # =================================================
        # 2. EXTRACT SECTIONS
        # =================================================

        sections = extract_sections(
            raw_text
        )

        word_count = calculate_word_count(
            raw_text
        )


        # =================================================
        # 3. BUILD PARSED RESUME
        # =================================================

        parsed_resume = {
            "raw_text": raw_text,
            "sections": sections,
            "word_count": word_count,
        }


        # =================================================
        # 4. BUILD CANDIDATE EVIDENCE
        # =================================================

        candidate_evidence = analyze_candidate_evidence(
            parsed_resume
        )


        # =================================================
        # 5. ATS ANALYSIS
        # =================================================

        ats_analysis = analyze_ats(
            parsed_resume,
            candidate_evidence
        )


        # =================================================
        # 6. RESUME IMPROVEMENTS
        # =================================================

        resume_improvements = analyze_resume_improvements(
            candidate_evidence,
            ats_analysis
        )


        # =================================================
        # 7. CHECK IF JOB DESCRIPTION EXISTS
        # =================================================

        has_job_description = bool(
            job_description.strip()
        )


        # =================================================
        # 8. JOB FIT OR CAREER DISCOVERY
        # =================================================

        if has_job_description:

            # ---------------------------------------------
            # JOB CONTEXT
            # ---------------------------------------------

            job_context = build_job_context(
                job_description
            )


            # ---------------------------------------------
            # JOB FIT ANALYSIS
            # ---------------------------------------------

            analysis_mode = "job_fit"

            career_analysis = analyze_job_fit(
                candidate_evidence,
                job_context
            )


            # ---------------------------------------------
            # GAP ACTION PLAN
            # ---------------------------------------------

            gap_action_plan = generate_gap_action_plan(
                candidate_evidence,
                job_context,
                career_analysis
            )

        else:

            # ---------------------------------------------
            # CAREER DISCOVERY
            # ---------------------------------------------

            analysis_mode = "career_discovery"

            job_context = None

            career_analysis = analyze_career_fit(
                candidate_evidence
            )

            # No JD means no job-specific gap analysis
            gap_action_plan = None


        # =================================================
        # 9. FINAL RESPONSE
        # =================================================

        return {
            "filename": resume.filename,

            "word_count": word_count,

            "sections_found": list(
                sections.keys()
            ),

            "analysis_mode": analysis_mode,

            "job_description_provided": has_job_description,

            "candidate_evidence": candidate_evidence,

            "job_context": job_context,

            "career_analysis": career_analysis,

            "ats_analysis": ats_analysis,

            "resume_improvements": resume_improvements,

            "gap_action_plan": gap_action_plan,
        }


    # =====================================================
    # FASTAPI ERRORS
    # =====================================================

    except HTTPException:
        raise


    # =====================================================
    # UNEXPECTED ERRORS
    # =====================================================

    except Exception as error:
        print(f"CareerPilot backend error: {error}")
        error_text = str(error).lower()

        if (
            "groq" in error_text
            or "api key" in error_text
            or "authentication" in error_text
            or "rate limit" in error_text
            or "429" in error_text
            or "503" in error_text
            or "service unavailable" in error_text
        ):
            raise HTTPException(
                status_code=503,
                detail=(
                    "AI analysis is temporarily unavailable. "
                    "Please try again in a moment."
            )
        )
        raise HTTPException(
            status_code=500,
            detail=(
                "CareerPilot couldn't complete the analysis. "
                "Please try again."
        )
    )