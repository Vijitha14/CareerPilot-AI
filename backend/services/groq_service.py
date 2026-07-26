import os
import json

from dotenv import load_dotenv
from groq import Groq


# Load environment variables from .env
load_dotenv()

# Get Groq API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY was not found in the .env file.")


# Create Groq client
client = Groq(api_key=api_key)


def analyze_career_fit(candidate_evidence):
    """
    Analyze the candidate's demonstrated resume evidence
    and identify career paths that currently fit them best.

    This is evidence-based analysis, not keyword counting.
    """

    prompt = f"""
You are the reasoning engine inside CareerPilot AI.

Your job is to analyze a candidate's resume and determine which
career paths their CURRENT resume demonstrates the strongest fit for.

IMPORTANT RULES:

1. Do NOT perform keyword counting.
2. Do NOT assume that listing a skill proves competency.
3. Give more importance to evidence from:
   - work experience
   - projects
   - open-source contributions
   - measurable achievements
4. Skills and certifications may support evidence, but should not
   be treated as strong proof by themselves.
5. Distinguish between:
   - demonstrated capability
   - partial evidence
   - claimed/listed skill
   - missing evidence
6. Do not invent experience that is not present in the resume.
7. Scores represent strength of demonstrated evidence,
   not probability of getting hired.

CANDIDATE RESUME EVIDENCE:

{json.dumps(candidate_evidence, indent=2)}

Analyze the candidate and return ONLY valid JSON in this exact structure:

{{
    "candidate_profile": "Short description of what kind of candidate this resume currently presents.",

    "demonstrated_capabilities": [
        {{
            "capability": "Capability name",
            "strength": "strong/moderate/limited",
            "evidence": [
                "Specific evidence from the resume"
            ],
            "reasoning": "Why this evidence supports the capability"
        }}
    ],

    "career_fits": [
        {{
            "role": "Career role",
            "fit_score": 0,
            "why": "Why the resume currently fits this role",
            "evidence": [
                "Specific supporting evidence"
            ],
            "gaps": [
                "Important capability not sufficiently demonstrated"
            ]
        }}
    ],

    "strongest_fit": {{
        "role": "Best fitting career role",
        "reason": "Why this is currently the strongest fit"
    }},

    "pilot_verdict": "Short, useful CareerPilot-style verdict."
}}

Return between 3 and 5 realistic career fits.
Rank career_fits from strongest to weakest.
fit_score must be between 0 and 100.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a rigorous career analysis engine. "
                    "Base conclusions only on evidence supplied in the resume."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    result_text = response.choices[0].message.content

    return json.loads(result_text)
def analyze_job_fit(candidate_evidence, job_context):
    """
    Analyze how well the candidate's demonstrated resume evidence
    fits a specific job.

    This uses evidence-based reasoning rather than keyword matching.
    """

    prompt = f"""
You are the job-fit reasoning engine inside CareerPilot AI.

Your task is to determine how well the candidate's ACTUAL demonstrated
experience fits the supplied job.

This is NOT keyword matching.

IMPORTANT RULES:

1. Do NOT calculate similarity using keyword overlap.
2. Do NOT give points simply because the same technology appears
   in both the resume and job description.
3. Evaluate whether the candidate has actually DEMONSTRATED the
   capabilities required by the job.
4. Give strongest weight to:
   - work experience
   - projects
   - open-source contributions
   - measurable achievements
5. Skills and certifications are supporting evidence only.
6. Distinguish between:
   - demonstrated capability
   - partial evidence
   - listed/claimed skill
   - missing evidence
7. Do not invent candidate experience.
8. Do not invent job requirements.
9. A missing preferred qualification should affect the score less
   than a missing core requirement.
10. The overall score represents strength of demonstrated fit,
    not probability of being hired.

CANDIDATE EVIDENCE:

{json.dumps(candidate_evidence, indent=2)}

JOB CONTEXT:

{json.dumps(job_context, indent=2)}

Return ONLY valid JSON using this exact structure:

{{
    "target_role": "Role inferred from the job",

    "overall_fit_score": 0,

    "fit_level": "strong/moderate/developing/weak",

    "summary": "Short explanation of the candidate's overall fit.",

    "requirement_analysis": [
        {{
            "requirement": "Important capability required by the job",
            "status": "demonstrated/partial/listed_only/missing",
            "evidence": [
                "Specific resume evidence supporting this assessment"
            ],
            "reasoning": "Why the evidence does or does not satisfy the requirement"
        }}
    ],

    "strongest_matches": [
        {{
            "capability": "Candidate strength relevant to this job",
            "evidence": "Specific evidence from the resume",
            "job_relevance": "Why this matters for this job"
        }}
    ],

    "critical_gaps": [
        {{
            "gap": "Important missing or insufficiently demonstrated capability",
            "importance": "high/medium/low",
            "reason": "Why this matters for this job"
        }}
    ],

    "transferable_strengths": [
        "Useful demonstrated capability that could transfer to this role"
    ],

    "recommendation": "strong_apply/apply/apply_with_improvements/build_skills_first",

    "pilot_verdict": "Short practical CareerPilot verdict explaining whether the candidate should pursue this job and what matters most."
}}

SCORING GUIDANCE:

85-100:
Strong demonstrated evidence for most important responsibilities.

70-84:
Good evidence for many core responsibilities with some meaningful gaps.

55-69:
Partial fit. Relevant foundation exists but several important capabilities
are not sufficiently demonstrated.

40-54:
Limited demonstrated alignment.

0-39:
Little evidence that the resume currently demonstrates the job's
core capabilities.

Do not inflate the score merely because technologies or keywords match.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a rigorous evidence-based job-fit analysis engine. "
                    "Compare demonstrated candidate capability against actual "
                    "job requirements. Never use simple keyword matching."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    result_text = response.choices[0].message.content

    return json.loads(result_text)

# =========================================================
# TEST WITH REAL RESUME
# =========================================================

if __name__ == "__main__":

    from parser_service import parse_resume
    from evidence_service import analyze_candidate_evidence

    pdf_path = "data/test_resume.pdf"

    # Parse resume
    with open(pdf_path, "rb") as file:
        parsed_resume = parse_resume(file)

    # Build candidate evidence
    candidate_evidence = analyze_candidate_evidence(parsed_resume)

    # Analyze career fit using Groq
    result = analyze_career_fit(candidate_evidence)

    print("\n" + "=" * 50)
    print("CAREERPILOT — CAREER DISCOVERY")
    print("=" * 50)

    print("\nCANDIDATE PROFILE:")
    print(result["candidate_profile"])

    print("\nCAREER FITS:")

    for career in result["career_fits"]:

        print(f"\n{career['role']} — {career['fit_score']}/100")

        print(f"Why: {career['why']}")

        print("Evidence:")
        for evidence in career["evidence"]:
            print(f"  - {evidence}")

        print("Gaps:")
        for gap in career["gaps"]:
            print(f"  - {gap}")

    print("\nSTRONGEST FIT:")
    print(result["strongest_fit"]["role"])
    print(result["strongest_fit"]["reason"])

    print("\nPILOT VERDICT:")
    print(result["pilot_verdict"])
def analyze_resume_improvements(candidate_evidence, ats_analysis):
    """
    Generate evidence-based resume improvement suggestions.
    """

    prompt = f"""
You are the resume improvement engine inside CareerPilot AI.

Your task is to identify practical improvements that would make the
candidate's resume stronger, clearer, and more convincing.

CANDIDATE EVIDENCE:

{json.dumps(candidate_evidence, indent=2)}

ATS ANALYSIS:

{json.dumps(ats_analysis, indent=2)}

IMPORTANT RULES:

1. Base suggestions only on information available in the resume analysis.
2. Never invent achievements, numbers, technologies, or experience.
3. Prioritize improvements that would materially strengthen the resume.
4. Distinguish between:
   - weak evidence
   - unclear writing
   - missing measurable impact
   - missing important information
5. Do not suggest adding experience the candidate does not have.
6. When suggesting a rewrite, preserve the original meaning.
7. Do not fabricate metrics in rewritten bullets.
8. Keep suggestions specific and actionable.

Return ONLY valid JSON using this exact structure:

{{
    "overall_assessment": "Short assessment of the resume.",

    "priority_improvements": [
        {{
            "area": "Area that needs improvement",
            "priority": "high/medium/low",
            "issue": "What is currently weak or unclear",
            "why_it_matters": "Why improving this would strengthen the resume",
            "action": "Specific thing the candidate should do"
        }}
    ],

    "bullet_improvements": [
        {{
            "current": "Existing resume statement if available",
            "problem": "What could be improved",
            "suggested_rewrite": "Improved version without inventing information"
        }}
    ],

    "strengths_to_keep": [
        "Existing resume strength that should remain"
    ],

    "next_best_action": "The single most useful improvement to make first."
}}

Return 3 to 6 priority improvements.

Only include bullet improvements when there is enough evidence to
rewrite them safely.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a rigorous resume improvement engine. "
                    "Never fabricate candidate achievements or experience."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    result_text = response.choices[0].message.content

    return json.loads(result_text)
def generate_gap_action_plan(candidate_evidence, job_context, job_fit_analysis):
    """
    Generate practical actions for the candidate's most important
    job-fit gaps.

    Actions must be grounded in the supplied resume evidence and
    actual job requirements.
    """

    prompt = f"""
You are the improvement-planning engine inside CareerPilot AI.

Your job is to turn a candidate's JOB FIT GAPS into a practical,
realistic action plan.

CANDIDATE EVIDENCE:

{json.dumps(candidate_evidence, indent=2)}

JOB CONTEXT:

{json.dumps(job_context, indent=2)}

JOB FIT ANALYSIS:

{json.dumps(job_fit_analysis, indent=2)}

IMPORTANT RULES:

1. Only address gaps that are relevant to the supplied job.
2. Prioritize gaps using their importance in the job-fit analysis.
3. Do not invent experience the candidate does not have.
4. Do not tell the candidate to falsely add skills to their resume.
5. Recommend actions that would create DEMONSTRABLE evidence.
6. Prefer practical actions such as:
   - improving an existing project
   - building a focused project feature
   - contributing to open source
   - deploying something
   - writing tests
   - demonstrating a technology through actual implementation
7. Avoid generic advice such as:
   "learn more", "practice coding", or "take a course"
   unless accompanied by a concrete deliverable.
8. Keep actions realistic for a student or early-career candidate.
9. Do not claim completing an action guarantees employment.
10. Rank the most important gaps first.

Return ONLY valid JSON in this exact structure:

{{
    "readiness_summary": "Short assessment of how close the candidate is to being well-aligned with this job.",

    "priority_actions": [
        {{
            "gap": "Capability currently missing or insufficiently demonstrated",

            "priority": "high/medium/low",

            "current_evidence": "What the resume currently demonstrates, if anything",

            "why_it_matters": "Why this capability matters for the supplied job",

            "action": "Specific practical action the candidate should take",

            "deliverable": "Concrete thing the candidate should produce or implement",

            "resume_evidence_after": "Example of the TYPE of evidence this work could legitimately create for the resume, without inventing results"
        }}
    ],

    "quick_wins": [
        "Small improvement that can strengthen alignment relatively quickly"
    ],

    "project_upgrade": {{
        "project_direction": "A practical way to upgrade an existing or new project to address important gaps",

        "capabilities_demonstrated": [
            "Capability this project upgrade would demonstrate"
        ]
    }},

    "next_best_action": "The single most useful next action for this candidate."
}}

Return no more than 5 priority actions.

If the candidate already demonstrates a capability strongly,
do not recommend rebuilding evidence for it.

Focus on turning missing capabilities into credible,
demonstrable resume evidence.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a rigorous career improvement planning engine. "
                    "Turn demonstrated job-fit gaps into concrete, ethical, "
                    "evidence-building actions."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    result_text = response.choices[0].message.content

    return json.loads(result_text)