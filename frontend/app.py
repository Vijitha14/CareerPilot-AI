import streamlit as st
import requests


# =========================================================
# CONFIG
# =========================================================

API_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="frontend/assets/cat_img.jpeg",
    layout="centered",
)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    html, body, [class*="css"] {
        font-family: Arial, "Helvetica Neue", Helvetica, sans-serif;
    }

    .block-container {
        padding-top: 4rem;
        padding-bottom: 3rem;
        max-width: 850px;
    }

    .hero-subtitle {
        text-align: center;
        font-size: 1.05rem;
        opacity: 0.65;
        margin-bottom: 2.5rem;
    }

    .footer {
        text-align: center;
        opacity: 0.45;
        font-size: 0.8rem;
        margin-top: 3rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HERO
# =========================================================

left, center, right = st.columns([1, 4, 1])

with center:

    logo_col, title_col = st.columns(
        [1, 5],
        vertical_alignment="center",
    )

    with logo_col:
        st.image(
            "frontend/assets/cat_img.jpeg",
            width=70,
        )

    with title_col:
        st.markdown(
            """
            <div style="
                font-size: 3rem;
                font-weight: 750;
                letter-spacing: -1.5px;
            ">
                CareerPilot AI
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="hero-subtitle" style="margin-top: 10px;">
            Resume analysis without the corporate headache.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# RESUME UPLOAD
# =========================================================

st.markdown("### Upload your resume")

uploaded_file = st.file_uploader(
    "Upload resume",
    type=["pdf"],
    label_visibility="collapsed",
)

if uploaded_file is None:

    st.caption("PDF · Max 10 MB")

else:

    st.success(
        f"Resume acquired — **{uploaded_file.name}** "
        f"({uploaded_file.size / 1024:.2f} KB)"
    )


# =========================================================
# JOB DESCRIPTION
# =========================================================

st.markdown("### Job description")

job_description = st.text_area(
    "Job description",
    placeholder=(
        "Paste the job description here...\n\n"
        "Leave this empty if you want CareerPilot "
        "to discover which careers your resume fits best."
    ),
    height=160,
    label_visibility="collapsed",
)

st.caption(
    "Optional — leave it blank for career discovery."
)


# =========================================================
# ANALYZE BUTTON
# =========================================================

analyze = st.button(
    "Analyze my resume →",
    type="primary",
    use_container_width=True,
)


# =========================================================
# BACKEND CONNECTION
# =========================================================

if analyze:

    if uploaded_file is None:

        st.warning(
            "Bestie... you forgot the resume. "
            "Upload the evidence first 😭"
        )

    else:

        try:

            with st.spinner(
                "Pilot is inspecting your career decisions..."
            ):

                uploaded_file.seek(0)

                files = {
                    "resume": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type,
                    )
                }

                data = {
                    "job_description": job_description
                }

                with st.spinner(
                    "Analyzing your resume... CareerPilot is reading your experience, skills, and projects."
                ):
                    response = requests.post(
                        API_URL,
                        files=files,
                        data=data,
                        timeout=120,
    )


            # =====================================================
            # SUCCESS
            # =====================================================

            if response.status_code == 200:

                result = response.json()

                st.success("Analysis complete!")


                # =================================================
                # RESUME OVERVIEW
                # =================================================

                st.markdown("---")
                st.markdown("## CareerPilot Analysis")

                overview_col1, overview_col2 = st.columns(2)

                with overview_col1:

                    st.metric(
                        "Resume words",
                        result.get("word_count", 0),
                    )

                with overview_col2:

                    st.metric(
                        "Sections detected",
                        len(
                            result.get(
                                "sections_found",
                                [],
                            )
                        ),
                    )


                # =================================================
                # GET CAREER ANALYSIS
                # =================================================

                career_analysis = result.get(
                    "career_analysis",
                    {},
                )

                analysis_mode = result.get(
                    "analysis_mode",
                    "career_discovery",
                )


                # =================================================
                # MODE 1 — CAREER DISCOVERY
                # =================================================

                if analysis_mode == "career_discovery":

                    st.markdown("### Career Discovery")

                    candidate_profile = career_analysis.get(
                        "candidate_profile",
                        "",
                    )

                    if candidate_profile:

                        st.markdown(
                            "#### Candidate profile"
                        )

                        st.write(
                            candidate_profile
                        )


                    # ---------------------------------------------
                    # CAREER FITS
                    # ---------------------------------------------

                    career_fits = career_analysis.get(
                        "career_fits",
                        [],
                    )

                    if career_fits:

                        st.markdown(
                            "### Your strongest career paths"
                        )

                        for fit in career_fits:

                            role = fit.get(
                                "role",
                                "Career",
                            )

                            score = fit.get(
                                "fit_score",
                                0,
                            )

                            why = fit.get(
                                "why",
                                "",
                            )

                            evidence = fit.get(
                                "evidence",
                                [],
                            )

                            gaps = fit.get(
                                "gaps",
                                [],
                            )

                            st.markdown(
                                f"#### {role} — {score}/100"
                            )

                            st.progress(
                                min(
                                    max(
                                        float(score) / 100,
                                        0.0,
                                    ),
                                    1.0,
                                )
                            )

                            if why:

                                st.write(
                                    why
                                )

                            if evidence:

                                with st.expander(
                                    "Why this fits you"
                                ):

                                    for item in evidence:

                                        st.markdown(
                                            f"- {item}"
                                        )

                            if gaps:

                                with st.expander(
                                    "What you're missing"
                                ):

                                    for gap in gaps:

                                        st.markdown(
                                            f"- {gap}"
                                        )


                    # ---------------------------------------------
                    # STRONGEST FIT
                    # ---------------------------------------------

                    strongest_fit = career_analysis.get(
                        "strongest_fit",
                        {},
                    )

                    if strongest_fit:

                        st.markdown("---")
                        st.markdown(
                            "### Strongest fit"
                        )

                        strongest_role = strongest_fit.get(
                            "role",
                            "",
                        )

                        strongest_reason = strongest_fit.get(
                            "reason",
                            "",
                        )

                        if strongest_role:

                            st.markdown(
                                f"## {strongest_role}"
                            )

                        if strongest_reason:

                            st.write(
                                strongest_reason
                            )


                    # ---------------------------------------------
                    # PILOT VERDICT
                    # ---------------------------------------------

                    pilot_verdict = career_analysis.get(
                        "pilot_verdict",
                        "",
                    )

                    if pilot_verdict:

                        st.markdown(
                            "### Pilot verdict"
                        )

                        st.info(
                            pilot_verdict
                        )


                # =================================================
                # MODE 2 — JOB FIT
                # =================================================

                elif analysis_mode == "job_fit":

                    target_role = career_analysis.get(
                        "target_role",
                        "Target Role",
                    )

                    score = career_analysis.get(
                        "overall_fit_score",
                        0,
                    )

                    fit_level = career_analysis.get(
                        "fit_level",
                        "",
                    )

                    summary = career_analysis.get(
                        "summary",
                        "",
                    )


                    # ---------------------------------------------
                    # JOB FIT HEADER
                    # ---------------------------------------------

                    st.markdown(
                        "### Job Fit Analysis"
                    )

                    st.markdown(
                        f"## {target_role}"
                    )


                    # ---------------------------------------------
                    # SCORE
                    # ---------------------------------------------

                    score_col, level_col = st.columns(2)

                    with score_col:

                        st.metric(
                            "Overall fit",
                            f"{score}/100",
                        )

                    with level_col:

                        st.metric(
                            "Fit level",
                            fit_level.title(),
                        )

                    st.progress(
                        min(
                            max(
                                float(score) / 100,
                                0.0,
                            ),
                            1.0,
                        )
                    )

                    if summary:

                        st.write(
                            summary
                        )


                    # ---------------------------------------------
                    # STRONGEST MATCHES
                    # ---------------------------------------------

                    strongest_matches = career_analysis.get(
                        "strongest_matches",
                        [],
                    )

                    if strongest_matches:

                        st.markdown(
                            "### Where you match"
                        )

                        for match in strongest_matches:

                            capability = match.get(
                                "capability",
                                "Capability",
                            )

                            evidence = match.get(
                                "evidence",
                                "",
                            )

                            relevance = match.get(
                                "job_relevance",
                                "",
                            )

                            st.markdown(
                                f"**✓ {capability}**"
                            )

                            if evidence:

                                st.caption(
                                    f"Evidence: {evidence}"
                                )

                            if relevance:

                                st.write(
                                    relevance
                                )


                    # ---------------------------------------------
                    # REQUIREMENT ANALYSIS
                    # ---------------------------------------------

                    requirements = career_analysis.get(
                        "requirement_analysis",
                        [],
                    )

                    if requirements:

                        st.markdown(
                            "### Requirement breakdown"
                        )

                        status_labels = {
                            "demonstrated": "✓ Demonstrated",
                            "partial": "◐ Partial evidence",
                            "listed_only": "○ Listed only",
                            "missing": "✕ Missing",
                        }

                        for requirement in requirements:

                            name = requirement.get(
                                "requirement",
                                "Requirement",
                            )

                            status = requirement.get(
                                "status",
                                "unknown",
                            )

                            evidence = requirement.get(
                                "evidence",
                                [],
                            )

                            reasoning = requirement.get(
                                "reasoning",
                                "",
                            )

                            status_text = status_labels.get(
                                status,
                                status.replace(
                                    "_",
                                    " ",
                                ).title(),
                            )

                            with st.expander(
                                f"{status_text} · {name}"
                            ):

                                if reasoning:

                                    st.write(
                                        reasoning
                                    )

                                if evidence:

                                    st.markdown(
                                        "**Resume evidence**"
                                    )

                                    for item in evidence:

                                        st.markdown(
                                            f"- {item}"
                                        )


                    # ---------------------------------------------
                    # CRITICAL GAPS
                    # ---------------------------------------------

                    critical_gaps = career_analysis.get(
                        "critical_gaps",
                        [],
                    )

                    if critical_gaps:

                        st.markdown(
                            "### Gaps to watch"
                        )

                        for gap in critical_gaps:

                            gap_name = gap.get(
                                "gap",
                                "",
                            )

                            importance = gap.get(
                                "importance",
                                "",
                            )

                            reason = gap.get(
                                "reason",
                                "",
                            )

                            if gap_name:

                                st.markdown(
                                    f"**{gap_name}**"
                                )

                            if importance:

                                st.caption(
                                    f"{importance.title()} priority"
                                )

                            if reason:

                                st.write(
                                    reason
                                )
                    # ---------------------------------------------
                    # GAP ACTION PLAN
                    # ---------------------------------------------

                    gap_action_plan = result.get(
                        "gap_action_plan",
                        {},
                    )

                    if gap_action_plan:

                        st.markdown("---")
                        st.markdown(
                            "## 🎯 Job Gap Action Plan"
                        )


                        # -----------------------------------------
                        # READINESS SUMMARY
                        # -----------------------------------------

                        readiness_summary = gap_action_plan.get(
                            "readiness_summary",
                            "",
                        )

                        if readiness_summary:

                            st.markdown(
                                "### Your readiness"
                            )

                            st.info(
                                readiness_summary
                            )


                        # -----------------------------------------
                        # PRIORITY ACTIONS
                        # -----------------------------------------

                        priority_actions = gap_action_plan.get(
                            "priority_actions",
                            [],
                        )

                        if priority_actions:

                            st.markdown(
                                "### What to work on"
                            )

                            priority_icons = {
                                "high": "🔴",
                                "medium": "🟡",
                                "low": "🟢",
                            }

                            for action_item in priority_actions:

                                gap = action_item.get(
                                    "gap",
                                    "Skill gap",
                                )

                                priority = action_item.get(
                                    "priority",
                                    "medium",
                                )

                                current_evidence = action_item.get(
                                    "current_evidence",
                                    "",
                                )

                                why_it_matters = action_item.get(
                                    "why_it_matters",
                                    "",
                                )

                                action = action_item.get(
                                    "action",
                                    "",
                                )

                                deliverable = action_item.get(
                                    "deliverable",
                                    "",
                                )

                                resume_evidence = action_item.get(
                                    "resume_evidence_after",
                                    "",
                                )

                                icon = priority_icons.get(
                                    priority.lower(),
                                    "•",
                                )

                                with st.expander(
                                    f"{icon} {priority.title()} priority · {gap}"
                                ):

                                    if current_evidence:

                                        st.markdown(
                                            "**What you already have**"
                                        )

                                        st.write(
                                            current_evidence
                                        )

                                    if why_it_matters:

                                        st.markdown(
                                            "**Why this matters**"
                                        )

                                        st.write(
                                            why_it_matters
                                        )

                                    if action:

                                        st.markdown(
                                            "**What to do next**"
                                        )

                                        st.success(
                                            action
                                        )

                                    if deliverable:

                                        st.markdown(
                                            "**Target deliverable**"
                                        )

                                        st.write(
                                            deliverable
                                        )

                                    if resume_evidence:

                                        st.markdown(
                                            "**Resume evidence you can earn**"
                                        )

                                        st.code(
                                            resume_evidence,
                                            language=None,
                                        )


                        # -----------------------------------------
                        # QUICK WINS
                        # -----------------------------------------

                        quick_wins = gap_action_plan.get(
                            "quick_wins",
                            [],
                        )

                        if quick_wins:

                            st.markdown(
                                "### ⚡ Quick wins"
                            )

                            for quick_win in quick_wins:

                                st.markdown(
                                    f"✓ {quick_win}"
                                )


                        # -----------------------------------------
                        # PROJECT UPGRADE
                        # -----------------------------------------

                        project_upgrade = gap_action_plan.get(
                            "project_upgrade",
                            {},
                        )

                        if project_upgrade:

                            st.markdown(
                                "### 🚀 Project upgrade"
                            )

                            project_direction = project_upgrade.get(
                                "project_direction",
                                "",
                            )

                            capabilities = project_upgrade.get(
                                "capabilities_demonstrated",
                                [],
                            )

                            if project_direction:

                                st.write(
                                    project_direction
                                )

                            if capabilities:

                                st.markdown(
                                    "**What this would demonstrate**"
                                )

                                for capability in capabilities:

                                    st.markdown(
                                        f"- {capability}"
                                    )


                        # -----------------------------------------
                        # NEXT BEST ACTION
                        # -----------------------------------------

                        next_best_action = gap_action_plan.get(
                            "next_best_action",
                            "",
                        )

                        if next_best_action:

                            st.markdown(
                                "### Your next move"
                            )

                            st.success(
                                next_best_action
                            )


                    # ---------------------------------------------
                    # TRANSFERABLE STRENGTHS
                    # ---------------------------------------------

                    transferable = career_analysis.get(
                        "transferable_strengths",
                        [],
                    )

                    if transferable:

                        st.markdown(
                            "### Transferable strengths"
                        )

                        for strength in transferable:

                            st.markdown(
                                f"- {strength}"
                            )


                    # ---------------------------------------------
                    # RECOMMENDATION
                    # ---------------------------------------------

                    recommendation = career_analysis.get(
                        "recommendation",
                        "",
                    )

                    recommendation_labels = {
                        "strong_apply": "Strong Apply",
                        "apply": "Apply",
                        "apply_with_improvements":
                            "Apply — but improve first",
                        "build_skills_first":
                            "Build skills first",
                    }

                    if recommendation:

                        st.markdown(
                            "### CareerPilot recommendation"
                        )

                        recommendation_text = (
                            recommendation_labels.get(
                                recommendation,
                                recommendation.replace(
                                    "_",
                                    " ",
                                ).title(),
                            )
                        )

                        st.success(
                            recommendation_text
                        )


                    # ---------------------------------------------
                    # PILOT VERDICT
                    # ---------------------------------------------

                    pilot_verdict = career_analysis.get(
                        "pilot_verdict",
                        "",
                    )

                    if pilot_verdict:

                        st.markdown(
                            "### Pilot verdict"
                        )

                        st.info(
                            pilot_verdict
                        )


                # =================================================
                # UNKNOWN ANALYSIS MODE
                # =================================================

                else:

                    st.warning(
                        "CareerPilot returned an unknown analysis mode."
                    )

                    st.json(
                        career_analysis
                    )


                # =================================================
                # ATS RESUME HEALTH
                # =================================================

                ats_analysis = result.get(
                    "ats_analysis",
                    {},
                )

                if ats_analysis:

                    st.markdown("---")
                    st.markdown(
                        "## ATS Resume Health"
                    )

                    ats_score = ats_analysis.get(
                        "ats_score",
                        0,
                    )

                    resume_length = ats_analysis.get(
                        "resume_length",
                        "unknown",
                    )

                    quantified_count = ats_analysis.get(
                        "quantified_achievement_count",
                        0,
                    )


                    # ---------------------------------------------
                    # ATS SCORE OVERVIEW
                    # ---------------------------------------------

                    ats_col1, ats_col2, ats_col3 = st.columns(3)

                    with ats_col1:

                        st.metric(
                            "ATS score",
                            f"{ats_score}/100",
                        )

                    with ats_col2:

                        st.metric(
                            "Resume length",
                            resume_length.title(),
                        )

                    with ats_col3:

                        st.metric(
                            "Quantified impact",
                            quantified_count,
                        )

                    st.progress(
                        min(
                            max(
                                float(ats_score) / 100,
                                0.0,
                            ),
                            1.0,
                        )
                    )


                    # ---------------------------------------------
                    # CONTACT CHECKS
                    # ---------------------------------------------

                    contact_checks = ats_analysis.get(
                        "contact_checks",
                        {},
                    )

                    if contact_checks:

                        st.markdown(
                            "### Contact & profile"
                        )

                        contact_columns = st.columns(
                            len(contact_checks)
                        )

                        for index, (name, found) in enumerate(
                            contact_checks.items()
                        ):

                            with contact_columns[index]:

                                icon = (
                                    "✓"
                                    if found
                                    else "✕"
                                )

                                st.markdown(
                                    f"**{icon} {name.title()}**"
                                )


                    # ---------------------------------------------
                    # SECTION CHECKS
                    # ---------------------------------------------

                    section_checks = ats_analysis.get(
                        "section_checks",
                        {},
                    )

                    if section_checks:

                        st.markdown(
                            "### Resume sections"
                        )

                        section_columns = st.columns(
                            len(section_checks)
                        )

                        for index, (section, found) in enumerate(
                            section_checks.items()
                        ):

                            with section_columns[index]:

                                icon = (
                                    "✓"
                                    if found
                                    else "✕"
                                )

                                st.markdown(
                                    f"**{icon} {section.title()}**"
                                )


                    # ---------------------------------------------
                    # ACTION VERBS
                    # ---------------------------------------------

                    action_verbs = ats_analysis.get(
                        "action_verbs_found",
                        [],
                    )

                    if action_verbs:

                        st.markdown(
                            "### Action-oriented writing"
                        )

                        st.write(
                            ", ".join(
                                verb.title()
                                for verb in action_verbs
                            )
                        )


                    # ---------------------------------------------
                    # ATS ISSUES
                    # ---------------------------------------------

                    issues = ats_analysis.get(
                        "issues",
                        [],
                    )

                    st.markdown(
                        "### ATS checks"
                    )

                    if issues:

                        for issue in issues:

                            st.warning(
                                issue
                            )

                    else:

                        st.success(
                            "No major structural ATS issues detected."
                        )


                # =================================================
                # RESUME IMPROVEMENTS
                # =================================================

                resume_improvements = result.get(
                    "resume_improvements",
                    {},
                )

                if resume_improvements:

                    st.markdown("---")
                    st.markdown(
                        "## Resume Improvements"
                    )


                    # ---------------------------------------------
                    # OVERALL ASSESSMENT
                    # ---------------------------------------------

                    overall_assessment = resume_improvements.get(
                        "overall_assessment",
                        "",
                    )

                    if overall_assessment:

                        st.markdown(
                            "### Overall assessment"
                        )

                        st.info(
                            overall_assessment
                        )


                    # ---------------------------------------------
                    # PRIORITY IMPROVEMENTS
                    # ---------------------------------------------

                    priority_improvements = resume_improvements.get(
                        "priority_improvements",
                        [],
                    )

                    if priority_improvements:

                        st.markdown(
                            "### What to improve first"
                        )

                        priority_icons = {
                            "high": "🔴",
                            "medium": "🟡",
                            "low": "🟢",
                        }

                        for improvement in priority_improvements:

                            area = improvement.get(
                                "area",
                                "Improvement",
                            )

                            priority = improvement.get(
                                "priority",
                                "medium",
                            )

                            issue = improvement.get(
                                "issue",
                                "",
                            )

                            why_it_matters = improvement.get(
                                "why_it_matters",
                                "",
                            )

                            action = improvement.get(
                                "action",
                                "",
                            )

                            icon = priority_icons.get(
                                priority.lower(),
                                "•",
                            )

                            with st.expander(
                                f"{icon} {priority.title()} priority · {area}"
                            ):

                                if issue:

                                    st.markdown(
                                        "**What's weak**"
                                    )

                                    st.write(
                                        issue
                                    )

                                if why_it_matters:

                                    st.markdown(
                                        "**Why it matters**"
                                    )

                                    st.write(
                                        why_it_matters
                                    )

                                if action:

                                    st.markdown(
                                        "**What to do**"
                                    )

                                    st.success(
                                        action
                                    )


                    # ---------------------------------------------
                    # BULLET IMPROVEMENTS
                    # ---------------------------------------------

                    bullet_improvements = resume_improvements.get(
                        "bullet_improvements",
                        [],
                    )

                    # Keep only valid bullet improvement objects
                    valid_bullet_improvements = []

                    if isinstance(bullet_improvements, list):

                        for bullet in bullet_improvements:

                            if not isinstance(bullet, dict):
                                continue

                            current = str(
                                bullet.get("current", "") or ""
                            ).strip()

                            problem = str(
                                bullet.get("problem", "") or ""
                            ).strip()

                            suggested = str(
                                bullet.get("suggested_rewrite", "") or ""
                            ).strip()

                            # Do not display completely empty AI responses
                            if current or problem or suggested:

                                valid_bullet_improvements.append(
                                    {
                                        "current": current,
                                        "problem": problem,
                                        "suggested_rewrite": suggested,
                                    }
                                )


                    if valid_bullet_improvements:

                        st.markdown(
                            "### Suggested bullet rewrites"
                        )

                        st.caption(
                            "Rewrites improve clarity and impact while "
                            "preserving information supported by your resume."
                        )

                        for index, bullet in enumerate(
                            valid_bullet_improvements,
                            start=1,
                        ):

                            current = bullet["current"]
                            problem = bullet["problem"]
                            suggested = bullet[
                                "suggested_rewrite"
                            ]

                            # -------------------------------------
                            # Better expander title
                            # -------------------------------------

                            if current:

                                preview = current

                                if len(preview) > 65:
                                    preview = preview[:65].rstrip() + "..."

                                expander_title = (
                                    f"Bullet {index} · {preview}"
                                )

                            else:

                                expander_title = (
                                    f"Bullet {index} · Suggested improvement"
                                )


                            with st.expander(
                                expander_title
                            ):

                                # ---------------------------------
                                # CURRENT BULLET
                                # ---------------------------------

                                if current:

                                    st.markdown(
                                        "**Current**"
                                    )

                                    st.write(
                                        current
                                    )

                                else:

                                    st.caption(
                                        "Original bullet was not returned "
                                        "by the analysis service."
                                    )


                                # ---------------------------------
                                # PROBLEM
                                # ---------------------------------

                                if problem:

                                    st.markdown(
                                        "**What's holding it back**"
                                    )

                                    st.write(
                                        problem
                                    )


                                # ---------------------------------
                                # SUGGESTED REWRITE
                                # ---------------------------------

                                if suggested:

                                    st.markdown(
                                        "**Suggested rewrite**"
                                    )

                                    st.success(
                                        suggested
                                    )


                                # ---------------------------------
                                # WHY IT'S BETTER
                                # ---------------------------------

                                if problem and suggested:

                                    st.markdown(
                                        "**Why it's better**"
                                    )

                                    st.write(
                                        "This version addresses the issue "
                                        f"identified above: {problem}"
                                    )
# ---------------------------------------------
                    # STRENGTHS TO KEEP
                    # ---------------------------------------------

                    strengths_to_keep = resume_improvements.get(
                        "strengths_to_keep",
                        [],
                    )

                    if strengths_to_keep:

                        st.markdown(
                            "### Strengths to keep"
                        )

                        for strength in strengths_to_keep:

                            st.markdown(
                                f"✓ {strength}"
                            )


                    # ---------------------------------------------
                    # NEXT BEST ACTION
                    # ---------------------------------------------

                    next_best_action = resume_improvements.get(
                        "next_best_action",
                        "",
                    )

                    if next_best_action:

                        st.markdown(
                            "### Your next move"
                        )

                        st.info(
                            next_best_action
                        )


            # =====================================================
            # BACKEND ERROR
            # =====================================================

            else:

                try:

                    error_message = response.json().get(
                        "detail",
                        response.text,
                    )

                except Exception:

                    error_message = response.text

                st.error(
                    f"Backend returned an error: {error_message}"
                )


        # =========================================================
        # CONNECTION ERROR
        # =========================================================

        except requests.exceptions.ConnectionError:

            st.error(
                "CareerPilot backend isn't running. "
                "Start FastAPI on port 8000 first."
            )


        # =========================================================
        # TIMEOUT
        # =========================================================

        except requests.exceptions.Timeout:

            st.error(
                "Analysis took too long. "
                "The AI service may be busy — try again."
            )


        # =========================================================
        # OTHER ERROR
        # =========================================================

        except Exception as error:

            st.error(
                f"Something went sideways: {error}"
            )


# =========================================================
# HOW IT WORKS
# =========================================================

st.markdown("---")
st.markdown("### How it works")

step1, step2, step3 = st.columns(3)


with step1:

    st.markdown("#### 01")
    st.markdown("**Upload**")

    st.caption(
        "Drop in your existing resume."
    )


with step2:

    st.markdown("#### 02")
    st.markdown("**Analyze**")

    st.caption(
        "CareerPilot examines your actual experience, "
        "projects and demonstrated skills."
    )


with step3:

    st.markdown("#### 03")
    st.markdown("**Improve**")

    st.caption(
        "Discover career fits, evaluate a specific job, "
        "and get practical resume improvements."
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        CareerPilot AI · Your AI Placement Copilot
    </div>
    """,
    unsafe_allow_html=True,
)
