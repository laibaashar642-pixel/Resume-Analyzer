# Resume Analyzer

### AI-Powered Resume Analysis and Job Matching

Resume Analyzer is a Django-based application that analyzes a resume against a job description and provides an explainable match report with skill gaps, semantic relevance, resume evidence, recommendations, and interview preparation.

## Features

* Resume PDF parsing and analysis
* Job description skill extraction
* Matched and missing skill detection
* Semantic similarity analysis
* Explainable match scoring
* Resume evidence and quality audit
* Personalized recommendations
* Interview question generation

## Architecture

```text
User
  │
  ▼
Django View
  │
  ├── PDF Parser
  ├── Resume Analyzer
  └── JD Analyzer
        │
        ▼
  Matching Engine
  │
  ├── Skill Matching
  ├── Semantic Similarity
  ├── Evidence Detection
  └── Score Calculation
        │
        ▼
  Recommendations
        │
        ▼
  Interview Generator
        │
        ▼
  Result Dashboard
```

The project follows a modular Django architecture, with core business logic separated into dedicated service modules.

## Scoring

The match score combines skill alignment and semantic relevance:

```text
Final Score =
    Skill Alignment × 60%
    +
    Semantic Similarity × 40%
```

Semantic similarity is calculated using:

```text
SentenceTransformer
       ↓
all-MiniLM-L6-v2
       ↓
Resume + Job Embeddings
       ↓
Cosine Similarity
```

## Tech Stack

* **Backend:** Python, Django
* **AI/NLP:** Sentence Transformers, Scikit-learn
* **PDF Processing:** PyMuPDF
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite
* **Version Control:** Git, GitHub

## Project Structure

```text
Analysis/
├── manage.py
├── Analysis/
└── home/
    ├── views.py
    ├── forms.py
    ├── services/
    │   ├── pdf_parser.py
    │   ├── resume_analyzer.py
    │   ├── jd_analyzer.py
    │   ├── matcher.py
    │   └── interview_generator.py
    ├── templates/
    └── static/
```

## Run Locally

```bash
git clone https://github.com/laibaashar642-pixel/Resume-Analyzer.git
cd Resume-Analyzer

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt

cd Analysis
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Project Status

**MVP Complete**

The current version supports resume analysis, job matching, semantic similarity, explainable scoring, resume auditing, recommendations, and interview preparation.

## Author

**Laiba Ashar Malik**
Agentic AI Developer

GitHub: https://github.com/laibaashar642-pixel
