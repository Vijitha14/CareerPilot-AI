def build_job_context(job_description, company_name=None):
    """
    Prepare job/company information for CareerPilot analysis.

    No keyword matching is performed here.
    The raw JD is passed to the AI so it can reason about
    responsibilities, expectations, seniority, and candidate evidence.
    """

    if not job_description or not job_description.strip():
        return None

    return {
        "job_description": job_description.strip(),
        "company_name": (
            company_name.strip()
            if company_name and company_name.strip()
            else None
        ),
    }