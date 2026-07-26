# 🐱 CareerPilot AI

**CareerPilot AI** is an AI-powered resume analysis and career discovery platform that helps candidates understand where their resume fits, evaluate ATS readiness, identify skill gaps, and compare their profile against a specific job description.

> Resume analysis without the corporate headache.

---

##  Live Application

**Frontend:**  
https://careerpilot-ai-vijitha.streamlit.app

**Backend:**  
Deployed using Render.

---

##  Features

###  Career Discovery
Upload a resume without providing a job description and CareerPilot AI analyzes the candidate's profile to:

- Identify suitable career paths
- Generate career-fit scores
- Explain why each career matches
- Highlight missing skills
- Recommend the strongest career fit
- Generate an AI-based candidate profile and verdict

###  ATS Resume Analysis

CareerPilot evaluates the overall health of the resume, including:

- ATS score
- Resume length
- Contact information detection
- LinkedIn and GitHub detection
- Resume section detection
- Action-oriented writing
- Quantified achievements
- Missing or weak sections

###  Job Description Matching

Users can optionally paste a job description to compare it against their resume.

The system analyzes:

- Resume-to-job compatibility
- Relevant skills
- Missing skills
- Candidate strengths
- Skill gaps
- Areas requiring improvement

###  Resume Improvement Suggestions

CareerPilot provides actionable recommendations to improve the resume based on detected weaknesses and AI analysis.

---

##  Tech Stack

### Frontend
- Streamlit
- Python

### Backend
- FastAPI
- Uvicorn
- Python

### AI
- Groq API
- Large Language Models (LLMs)

### Resume Processing
- PyMuPDF
- PDF text extraction and parsing

### Communication
- REST API
- Requests

### Deployment
- Streamlit Community Cloud — Frontend
- Render — FastAPI Backend

### Version Control
- Git
- GitHub

---

##  System Architecture

```text
User
 │
 ▼
Streamlit Frontend
 │
 │ Resume PDF + Optional Job Description
 ▼
FastAPI Backend
 │
 ├── Resume Parser
 │      │
 │      └── Extract Resume Text
 │
 ├── ATS Analysis
 │
 ├── Evidence Analysis
 │
 ├── Career / Job Analysis
 │
 └── Groq AI Service
        │
        ▼
     LLM Analysis
        │
        ▼
Structured Results
 │
 ▼
Streamlit Dashboard
```

---

##  Project Structure

```text
CareerPilot-AI/
│
├── backend/
│   ├── services/
│   │   ├── ats_service.py
│   │   ├── evidence_service.py
│   │   ├── groq_service.py
│   │   ├── job_service.py
│   │   └── parser_service.py
│   │
│   ├── main.py
│   ├── database/
│   ├── models/
│   ├── prompts/
│   └── routes/
│
├── frontend/
│   ├── assets/
│   │   └── cat_img.jpeg
│   ├── app.py
│   ├── components/
│   └── pages/
│
├── data/
│
├── tests/
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ How It Works

### 1. Upload Resume

The user uploads a resume in PDF format through the Streamlit interface.

### 2. Extract Resume Content

The PDF is sent to the FastAPI backend where PyMuPDF extracts and processes the resume text.

### 3. Analyze Candidate Profile

CareerPilot analyzes the candidate's:

- Skills
- Projects
- Education
- Experience
- Resume structure
- Career evidence

### 4. AI Analysis

Extracted resume information is processed using the Groq API to generate career recommendations and contextual feedback.

### 5. ATS Evaluation

The system evaluates resume quality and identifies missing sections, weak areas, and opportunities for improvement.

### 6. Display Results

The structured analysis is returned to the Streamlit frontend and displayed as an interactive CareerPilot Analysis dashboard.

---

##  Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/Vijitha14/CareerPilot-AI.git
cd CareerPilot-AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

> Never commit your `.env` file or API keys to GitHub.

### 5. Start the FastAPI backend

```bash
uvicorn backend.main:app --reload
```

Backend runs locally at:

```text
http://127.0.0.1:8000
```

### 6. Start the Streamlit frontend

Open another terminal:

```bash
streamlit run frontend/app.py
```

The application will normally open at:

```text
http://localhost:8501
```

---

##  Environment Variables

CareerPilot requires:

```env
GROQ_API_KEY=your_groq_api_key
```

For production deployment, environment variables should be configured through the deployment platform rather than committed to the repository.

---

## ☁️ Deployment

CareerPilot uses separate frontend and backend deployments.

```text
Streamlit Community Cloud
        │
        │ HTTPS API Request
        ▼
Render
FastAPI Backend
        │
        ▼
Groq API
```

The Streamlit frontend communicates with the deployed FastAPI REST API hosted on Render.

---



## 🔮 Future Improvements

- User authentication
- Resume history
- Multiple resume comparison
- Improved ATS keyword matching
- Resume rewriting suggestions
- Downloadable analysis reports
- Career roadmap generation
- Job recommendation integration
- Resume version tracking

---

## ⚠️ Disclaimer

CareerPilot AI provides AI-assisted resume and career analysis. Scores and recommendations should be treated as guidance rather than guarantees of hiring outcomes or ATS performance.

---

##  Author

**Glory Vijitha**

Computer Science & Engineering

GitHub: `Vijitha14`

---

## ⭐ Support

If you find CareerPilot AI useful, consider giving the repository a ⭐ on GitHub.
