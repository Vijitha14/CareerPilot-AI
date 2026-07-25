import re


def analyze_ats(parsed_resume, candidate_evidence):
    """
    Perform deterministic ATS-oriented checks on a parsed resume.

    This layer checks resume structure and basic ATS compatibility.
    Deeper qualitative feedback can be added through the AI layer later.
    """

    raw_text = parsed_resume.get("raw_text", "")
    sections = parsed_resume.get("sections", {})
    word_count = parsed_resume.get("word_count", 0)

    text_lower = raw_text.lower()

    # -------------------------------------------------
    # Contact information
    # -------------------------------------------------

    email_found = bool(
        re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            raw_text,
        )
    )

    phone_found = bool(
        re.search(
            r"(?:\+?\d[\d\s\-()]{8,}\d)",
            raw_text,
        )
    )

    linkedin_found = (
        "linkedin.com" in text_lower
        or "linkedin" in text_lower
    )

    github_found = (
        "github.com" in text_lower
        or "github" in text_lower
    )

    # -------------------------------------------------
    # Important resume sections
    # -------------------------------------------------

    detected_sections = {
        str(section).lower()
        for section in sections.keys()
    }

    section_checks = {
        "summary": any(
            name in detected_sections
            for name in ["summary", "profile", "objective"]
        ),

        "experience": any(
            name in detected_sections
            for name in [
                "experience",
                "work experience",
                "internships",
            ]
        ),

        "projects": any(
            name in detected_sections
            for name in ["projects", "project"]
        ),

        "skills": any(
            name in detected_sections
            for name in [
                "skills",
                "technical_skills",
                "technical skills",
                "technologies",
                "tools",
                "programming languages",
                "languages",
            ]
        ),

        "education": any(
            name in detected_sections
            for name in ["education", "academic"]
        ),
    }

    # -------------------------------------------------
    # Quantified achievements
    # -------------------------------------------------

    quantified_patterns = re.findall(
        r"\b\d+(?:\.\d+)?%|\b\d+\+|\b\d+x\b",
        raw_text,
        flags=re.IGNORECASE,
    )

    quantified_achievement_count = len(
        quantified_patterns
    )

    # -------------------------------------------------
    # Action verbs
    # -------------------------------------------------

    action_verbs = [
        "built",
        "developed",
        "designed",
        "implemented",
        "created",
        "automated",
        "improved",
        "optimized",
        "integrated",
        "deployed",
        "engineered",
        "led",
        "managed",
        "reduced",
        "increased",
        "delivered",
        "contributed",
    ]

    action_verbs_found = sorted(
        {
            verb
            for verb in action_verbs
            if re.search(
                rf"\b{re.escape(verb)}\b",
                text_lower,
            )
        }
    )

    # -------------------------------------------------
    # Resume length
    # -------------------------------------------------

    if 300 <= word_count <= 800:
        length_status = "good"

    elif word_count < 300:
        length_status = "short"

    else:
        length_status = "long"

    # -------------------------------------------------
    # Deterministic ATS score
    # -------------------------------------------------

    score = 0

    # Contact details: 15
    if email_found:
        score += 5

    if phone_found:
        score += 5

    if linkedin_found or github_found:
        score += 5

    # Important sections: 35
    score += sum(
        7
        for present in section_checks.values()
        if present
    )

    # Resume length: 10
    if length_status == "good":
        score += 10
    elif length_status == "short":
        score += 5
    else:
        score += 6

    # Action-oriented writing: 20
    if len(action_verbs_found) >= 8:
        score += 20
    elif len(action_verbs_found) >= 5:
        score += 15
    elif len(action_verbs_found) >= 3:
        score += 10
    elif action_verbs_found:
        score += 5

    # Quantified achievements: 20
    if quantified_achievement_count >= 5:
        score += 20
    elif quantified_achievement_count >= 3:
        score += 15
    elif quantified_achievement_count >= 1:
        score += 8

    score = min(score, 100)

    # -------------------------------------------------
    # Issues
    # -------------------------------------------------

    issues = []

    if not email_found:
        issues.append("Email address was not detected.")

    if not phone_found:
        issues.append("Phone number was not detected.")

    for section, present in section_checks.items():
        if not present:
            issues.append(
                f"{section.title()} section was not clearly detected."
            )

    if quantified_achievement_count == 0:
        issues.append(
            "No clearly quantified achievements were detected."
        )

    if len(action_verbs_found) < 3:
        issues.append(
            "Resume contains limited evidence of action-oriented bullet writing."
        )

    if length_status == "short":
        issues.append(
            "Resume may be too short to demonstrate enough experience and impact."
        )

    elif length_status == "long":
        issues.append(
            "Resume may contain more text than necessary."
        )

    return {
        "ats_score": score,

        "word_count": word_count,

        "resume_length": length_status,

        "contact_checks": {
            "email": email_found,
            "phone": phone_found,
            "linkedin": linkedin_found,
            "github": github_found,
        },

        "section_checks": section_checks,

        "action_verbs_found": action_verbs_found,

        "quantified_achievement_count": quantified_achievement_count,

        "issues": issues,
    }