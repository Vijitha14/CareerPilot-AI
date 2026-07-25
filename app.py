import streamlit as st




st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="frontend/assets/cat_img.jpeg",
    layout="centered",
)




st.markdown("""
<style>

/* Main font */
html, body, [class*="css"] {
    font-family: Arial, "Helvetica Neue", Helvetica, sans-serif;
}

/* Give page comfortable spacing */
.block-container {
    padding-top: 4rem;
    padding-bottom: 3rem;
    max-width: 850px;
}

/* Main title */
.hero-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 750;
    letter-spacing: -1.5px;
    margin-bottom: 5px;
}

/* Hero subtitle */
.hero-subtitle {
    text-align: center;
    font-size: 1.05rem;
    opacity: 0.65;
    margin-bottom: 2.5rem;
}

/* Small footer */
.footer {
    text-align: center;
    opacity: 0.45;
    font-size: 0.8rem;
    margin-top: 3rem;
}

</style>
""", unsafe_allow_html=True)




# ---------- Hero Section ----------

left, center, right = st.columns([1, 4, 1])

with center:
    logo_col, title_col = st.columns([1, 5], vertical_alignment="center")

    with logo_col:
        st.image(
            "frontend/assets/cat_img.jpeg",
            width=70
        )

    with title_col:
        st.markdown(
            "<div style='font-size: 3rem; font-weight: 750; "
            "letter-spacing: -1.5px;'>CareerPilot AI</div>",
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="hero-subtitle" style="margin-top: 10px;">
            Resume analysis without the corporate headache.
        </div>
        """,
        unsafe_allow_html=True,
    )




st.markdown("###  Upload your resume")

uploaded_file = st.file_uploader(
    "Upload resume",
    type=["pdf", "docx"],
    label_visibility="collapsed",
)

if uploaded_file is None:

    st.caption(
        "PDF or DOCX · Max 10 MB"
    )

else:

    st.success(
        f"Resume acquired — **{uploaded_file.name}** ({uploaded_file.type}, {uploaded_file.size / 1024:.2f} KB)"
    )





st.markdown("###  Job description")

job_description = st.text_area(
    "Job description",
    placeholder=(
        "Paste the job description here...\n\n"
        "We'll compare your resume against the role."
    ),
    height=160,
    label_visibility="collapsed",
)

st.caption(
    "Optional — but adding a job description gives you a much more accurate match score."
)


analyze = st.button(
    "Analyze my resume →",
    type="primary",
    use_container_width=True,
)




if analyze:

    if uploaded_file is None:

        st.warning("Bestie... you forgot the resume upload. Please upload your resume first.")

    else:

        with st.spinner(
            "Pilot is inspecting your career decisions... This may take a few seconds."
        ):

            # Backend will be connected here later.
            pass

        st.success("Analysis complete!")

        st.info(
            "Your actual ATS score and AI feedback will appear here once "
            "we connect the backend."
        )




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
        "CareerPilot checks ATS compatibility, skills and job relevance."
    )


with step3:

    st.markdown("#### 03")
    st.markdown("**Improve**")

    st.caption(
        "Get actionable suggestions instead of generic AI yapping."
    )




st.markdown(
    """
    <div class="footer">
        CareerPilot AI · Your AI Placement Copilot ✈️
    </div>
    """,
    unsafe_allow_html=True,
)