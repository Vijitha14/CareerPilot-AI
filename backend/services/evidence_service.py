"""
Candidate evidence preparation service.

This service takes the structured resume produced by
parser_service.py and prepares the candidate's actual
resume evidence for AI analysis.

It does NOT perform keyword matching or scoring.
"""


def analyze_candidate_evidence(parsed_resume):
    """
    Organize evidence from the candidate's resume so that
    the AI can reason about what the candidate has actually
    demonstrated.

    Args:
        parsed_resume (dict):
            Structured resume returned by parse_resume().

    Returns:
        dict:
            Candidate evidence grouped by resume section.
    """

    # Get the sections extracted by parser_service.py
    sections = parsed_resume.get("sections", {})

    # Collect useful evidence from the resume
    candidate_context = {
        "summary": sections.get("summary", ""),
        "skills": sections.get("technical_skills", ""),
        "experience": sections.get("experience", ""),
        "projects": sections.get("projects", ""),
        "open_source": sections.get("open_source", ""),
        "education": sections.get("education", ""),
        "certifications": sections.get("certifications", ""),
    }

    return candidate_context


# =========================================================
# TEMPORARY TEST
# =========================================================

if __name__ == "__main__":

    sample_resume = {
        "sections": {
            "summary": "Computer Science student with experience in AI and software development.",

            "technical_skills": "Python, Java, SQL, FastAPI, Streamlit",

            "experience": (
                "Built automation systems and AI applications "
                "during technical internships."
            ),

            "projects": (
                "Built CareerPilot AI, an AI-powered resume "
                "analysis platform."
            ),

            "open_source": (
                "Contributed multiple pull requests to "
                "open-source projects."
            ),

            "education": (
                "B.E. Computer Science and Engineering."
            ),

            "certifications": (
                "Python, SQL and Generative AI certifications."
            ),
        }
    }

    evidence = analyze_candidate_evidence(sample_resume)

    print("\n" + "=" * 50)
    print("CANDIDATE EVIDENCE")
    print("=" * 50)

    for section, content in evidence.items():
        print(f"\n{section.upper()}")
        print("-" * 30)
        print(content)