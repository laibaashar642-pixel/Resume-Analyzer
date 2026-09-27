CareerMatch AI

An AI-powered resume analysis and job matching platform that helps candidates understand how well their resume aligns with a job description — and, more importantly, why.

CareerMatch AI analyzes a candidate's resume PDF and a target job description to produce an explainable match report containing:

Resume skill detection

Job-description skill extraction

Semantic similarity analysis

Explainable match score

Matched and missing skills

Resume evidence for detected skills

Resume quality audit

Personalized recommendations

Smart interview preparation questions

Table of Contents

Overview

Why CareerMatch AI

Key Features

System Architecture

Application Flow

Scoring System

Project Structure

Technology Stack

How Each Layer Works

Installation

Running Locally

Using the Application

Testing

Production / Deployment

Limitations

Future Improvements

Author

Overview

CareerMatch AI is a Django-based resume intelligence application.

A traditional resume checker may simply tell a candidate:

"Your resume matches this job by 72%."

CareerMatch AI goes further by explaining:

Which required skills were detected

Which skills are missing

Which resume lines provide evidence

How semantically relevant the resume is to the job description

What areas the candidate should improve

What questions they should prepare for before an interview

The goal is to make the result transparent and actionable instead of being just a single percentage.

Why CareerMatch AI?

Job descriptions can contain many requirements, and manually comparing them with a resume is time-consuming.

CareerMatch AI automates this process through a pipeline:

Resume PDF
    +
Job Description
    ↓
PDF Text Extraction
    ↓
Resume Analysis + Skill Detection
    +
Job Description Analysis
    ↓
Skill Matching
    +
Semantic Similarity
    ↓
Explainable Match Score
    ↓
Evidence + Gaps + Recommendations
    ↓
Interview Preparation

Key Features

1. Resume PDF Parsing

The application accepts a resume in PDF format and extracts readable text using PyMuPDF.

It also performs basic validation:

PDF format validation

File-size validation

Empty/unreadable PDF detection

2. Resume Analysis

The extracted resume text is analyzed to identify:

Candidate name

Email

Phone number

Technical skills

Resume sections

The skill detector currently covers technologies and concepts across:

Python

Django

Django REST Framework

FastAPI

Flask

SQL

PostgreSQL

MySQL

Oracle

JavaScript

HTML

CSS

React

Node.js

C/C++

Machine Learning

Deep Learning

Artificial Intelligence

Computer Vision

OpenCV

MediaPipe

YOLO

PyTorch

TensorFlow

NumPy

Pandas

Scikit-learn

LangChain

LangGraph

RAG

LLMs

Embeddings

ChromaDB

FAISS

Git

GitHub

Docker

REST APIs

The skill list is configurable and can be extended as the project grows.

3. Job Description Analysis

The job description is processed using the same normalized skill-detection approach.

The system extracts:

Required skills

Number of detected skills

Job-description word count

This creates a structured representation of the job requirements.

4. Semantic Similarity

Keyword matching alone is not enough.

For example, two texts can describe similar work without using exactly the same words.

CareerMatch AI therefore uses:

SentenceTransformer
        ↓
all-MiniLM-L6-v2
        ↓
Resume Embedding
        +
Job Description Embedding
        ↓
Cosine Similarity

The resulting similarity is converted into a percentage.

This provides a second signal representing the overall semantic relationship between the resume and the job description.

5. Explainable Match Score

The final score is intentionally deterministic.

Current scoring formula:

Final Score =
    Skill Score × 60%
    +
    Semantic Score × 40%

For example:

Skill Score     = 80
Semantic Score  = 70

Final Score =
    (80 × 0.60) + (70 × 0.40)
    = 76

This approach keeps the score reproducible and explainable.

The application does not rely on a generative model to randomly decide the candidate's score.

6. Matched Skills

The system calculates:

Resume Skills ∩ Job Skills

These skills are displayed as matched skills.

Example:

Matched:
- Python
- Django
- PostgreSQL
- LangChain

7. Missing Skills

The system calculates:

Job Skills - Resume Skills

Example:

Missing:
- Docker
- FastAPI
- Kubernetes

This gives the candidate a clear skill-gap view.

8. Resume Evidence

For every matched skill, CareerMatch AI tries to find the actual resume line where the skill appears.

Example:

Skill:
Django

Evidence:
"Developed REST APIs using Django REST Framework..."

This makes the result more transparent than simply showing a list of detected skills.

9. Resume Audit

The application checks whether important resume sections are present.

Current audit areas include:

Summary

Skills

Experience

Projects

Education

Certifications

This helps identify structural weaknesses in the resume.

10. Recommendations

Recommendations are generated from the analysis results.

For example:

Strengthen missing technical skills

Improve alignment with the job description

Review specific technologies

Maintain strong semantic relevance

The recommendations are based on detected gaps rather than arbitrary advice.

11. Smart Interview Preparation

CareerMatch AI generates interview questions using:

Matched skills

Missing skills

Backend/API concepts

Project experience

Scalability and maintainability topics

Debugging concepts

Each question can contain:

Question
Why this question matters
What to prepare

This turns the resume analysis into an interview-preparation workflow.

System Architecture

CareerMatch AI follows a modular Django architecture.

                    ┌─────────────────────────┐
                    │       User / Browser     │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      Django Views       │
                    │       views.py           │
                    └────────────┬────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 │                               │
                 ▼                               ▼
       ┌──────────────────┐           ┌──────────────────┐
       │   PDF Parser     │           │  JD Analyzer     │
       │  pdf_parser.py   │           │ jd_analyzer.py   │
       └────────┬─────────┘           └────────┬─────────┘
                │                              │
                ▼                              ▼
       ┌──────────────────┐           ┌──────────────────┐
       │ Resume Analyzer  │           │ Required Skills  │
       │resume_analyzer.py│           │      + count      │
       └────────┬─────────┘           └────────┬─────────┘
                │                              │
                └──────────────┬───────────────┘
                               ▼
                    ┌─────────────────────────┐
                    │        Matcher          │
                    │      matcher.py         │
                    ├─────────────────────────┤
                    │ Skill Matching           │
                    │ Semantic Similarity      │
                    │ Evidence Detection       │
                    │ Score Calculation        │
                    │ Explanation              │
                    │ Recommendations          │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ Interview Generator     │
                    │ interview_generator.py  │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      Result Dashboard   │
                    │       result.html       │
                    └─────────────────────────┘

Application Flow

Step 1 — User Uploads Resume

The user uploads a PDF resume and enters a job description.

POST /

Django receives:

request.POST
request.FILES

The form validates the input.

Step 2 — PDF Text Extraction

The uploaded PDF is passed to:

home/services/pdf_parser.py

The parser:

Reads PDF bytes

Opens the PDF with PyMuPDF

Extracts text page by page

Removes empty lines

Returns cleaned text

Raises a user-friendly error if no readable text exists

Step 3 — Resume Analysis

The cleaned resume text is passed to:

analyze_resume()

The analyzer detects:

Candidate Information
        +
Skills
        +
Resume Sections

Step 4 — Resume Audit

The resume is also passed through:

generate_resume_audit()

This checks the presence of important resume sections.

Step 5 — Job Description Analysis

The job description is passed to:

analyze_job_description()

The analyzer extracts the required skills.

Step 6 — Skill Matching

The matcher compares:

Resume Skills
       vs
Required Job Skills

Using set operations:

matched = resume_skills.intersection(required_skills)

missing = required_skills.difference(resume_skills)

Step 7 — Semantic Matching

The complete resume text and job description are converted into embeddings using:

all-MiniLM-L6-v2

Cosine similarity is then calculated.

Step 8 — Final Score

The skill score and semantic score are combined:

60% Skill Alignment
40% Semantic Relevance

The result is shown as the overall match percentage.

Step 9 — Evidence

For each matched skill, the system searches the resume for a supporting line.

Step 10 — Explanation

The system generates a human-readable explanation covering:

Technical alignment

Semantic relevance

Missing skills

Step 11 — Recommendations

The missing skills and semantic score are used to create improvement recommendations.

Step 12 — Interview Preparation

The application generates up to 10 interview questions based on:

Matched Skills
Missing Skills
Backend Concepts
Project Experience
Scalability
Debugging

Step 13 — Result Dashboard

All results are passed to:

home/templates/home/result.html

The dashboard displays the complete analysis.

Project Structure

Resume-Analyzer/
│
├── Analysis/
│   ├── manage.py
│   │
│   ├── Analysis/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   ├── wsgi.py
│   │   └── __init__.py
│   │
│   └── home/
│       ├── admin.py
│       ├── apps.py
│       ├── forms.py
│       ├── models.py
│       ├── tests.py
│       ├── urls.py
│       ├── views.py
│       │
│       ├── services/
│       │   ├── pdf_parser.py
│       │   ├── resume_analyzer.py
│       │   ├── jd_analyzer.py
│       │   ├── matcher.py
│       │   └── interview_generator.py
│       │
│       ├── templates/
│       │   └── home/
│       │       ├── home.html
│       │       ├── upload.html
│       │       └── result.html
│       │
│       └── static/
│           └── home/
│               ├── css/
│               │   └── style.css
│               └── js/
│                   └── app.js
│
├── requirements.txt
├── .gitignore
├── README.md
└── .env

Technology Stack

Backend

Python

Django

AI / NLP

Sentence Transformers

all-MiniLM-L6-v2

Scikit-learn

Cosine similarity

PDF Processing

PyMuPDF

Frontend

HTML

CSS

JavaScript

Development / Version Control

Git

GitHub

Virtual Environment

Database

SQLite for the current development/demo setup

How Each Layer Works

views.py

The view acts as the application orchestrator.

It connects all services:

Form
 ↓
PDF Parser
 ↓
Resume Analyzer
 ↓
Resume Audit
 ↓
JD Analyzer
 ↓
Matcher
 ↓
Explanation
 ↓
Recommendations
 ↓
Interview Generator
 ↓
Result Template

The business logic is intentionally kept outside the view as much as possible.

pdf_parser.py

Responsible only for PDF extraction.

PDF
 ↓
PyMuPDF
 ↓
Raw Text
 ↓
Clean Text

resume_analyzer.py

Responsible for understanding the resume.

It detects:

Skills
Email
Phone
Resume Sections

It also provides the resume audit functionality.

jd_analyzer.py

Responsible for converting a raw job description into structured information.

Job Description
        ↓
Skill Detection
        ↓
Required Skills
        +
Word Count

matcher.py

This is the core matching engine.

It handles:

Skill Matching
Semantic Similarity
Evidence Detection
Score Calculation
Match Explanation
Recommendations

The score calculation is deterministic and therefore reproducible.

interview_generator.py

Uses the analysis output to generate interview preparation questions.

The questions are connected to the actual detected skills and job requirements.

Installation

1. Clone the repository

git clone https://github.com/laibaashar642-pixel/Resume-Analyzer.git
cd Resume-Analyzer

To use the current development branch:

git checkout ai-resume-mpv

2. Create a virtual environment

Windows

python -m venv .venv
.venv\Scripts\activate

macOS / Linux

python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Move into the Django project directory

cd Analysis

5. Run migrations

python manage.py migrate

6. Start the development server

python manage.py runserver

Open:

http://127.0.0.1:8000/

Using the Application

Step 1

Open the application.

Step 2

Upload a resume PDF.

Step 3

Paste the target job description.

Step 4

Submit the form.

Step 5

Review:

Overall Match Score
        ↓
Skill Score
        ↓
Semantic Score
        ↓
Why This Score?
        ↓
Resume Audit
        ↓
Matched Skills
        ↓
Missing Skills
        ↓
Resume Evidence
        ↓
Recommendations
        ↓
Interview Preparation

Testing

Basic Django system checks:

python manage.py check

Run the application:

python manage.py runserver

The current MVP has been tested locally for:

Django system checks

Home page response

Resume upload flow

Job description submission

Result page rendering

Static CSS loading

Resume analysis

Skill matching

Semantic similarity

Match score calculation

Recommendations

Interview question generation

Production / Deployment

The application is designed to be deployable as a Django web service.

For a production deployment, the following should be configured:

GitHub Repository
       ↓
Cloud Web Service
       ↓
Install requirements
       ↓
Django collectstatic
       ↓
Django migrations
       ↓
Gunicorn
       ↓
Analysis.wsgi:application

Important production settings include:

DEBUG=False

Secure SECRET_KEY

Correct ALLOWED_HOSTS

Static-file configuration

Gunicorn

WhiteNoise or another static-file solution

Environment variables for secrets

Production database when persistent data is required

The current demo uses SQLite. SQLite data on an ephemeral cloud filesystem should not be treated as permanent production storage.

Environment Variables

Sensitive configuration should be stored in environment variables rather than committed to GitHub.

Example:

SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain

The .env file is excluded from Git using .gitignore.

Never commit real API keys, passwords, SMTP credentials, or other secrets.

Design Principles

Explainability

The application does not only return:

72%

It also provides:

Why?
What matched?
What is missing?
Where is the evidence?
What should I improve?
What should I prepare for?

Deterministic Scoring

The final score is calculated using explicit rules.

Final Score =
60% Skill Alignment
+
40% Semantic Similarity

This makes the scoring process easier to understand and test.

Modular Architecture

Each major responsibility has its own service.

PDF processing      → pdf_parser.py
Resume analysis     → resume_analyzer.py
JD analysis         → jd_analyzer.py
Matching            → matcher.py
Interview prep      → interview_generator.py

This makes the codebase easier to maintain and extend.

Current Limitations

CareerMatch AI is currently an MVP.

Some limitations include:

Skill detection depends on the configured skill dictionary.

Keyword matching can miss synonyms that are not represented in the skill list.

PDF extraction quality depends on the structure of the uploaded PDF.

Semantic similarity represents overall text relevance and should not be treated as a complete measure of candidate suitability.

The current score is a transparent engineering metric, not a hiring decision.

Resume evidence currently searches for matching skill text in resume lines.

SQLite is currently intended for development/demo usage.

Future Improvements

Planned improvements include:

Advanced NLP

Skill synonym normalization

Context-aware skill extraction

Experience-level detection

Better section parsing

Entity extraction

AI Features

LLM-powered resume rewriting

Personalized cover-letter generation

More advanced interview simulation

Conversational career assistant

Job-specific resume optimization

Matching Engine

Experience-weighted scoring

Education matching

Project relevance scoring

Role/title similarity

Seniority detection

Industry-specific matching

Backend

PostgreSQL production database

REST API

Authentication

User profiles

Saved analyses

Analysis history

Infrastructure

Docker

CI/CD

Cloud deployment

Background processing

Caching

Monitoring

Logging

Frontend

Interactive score visualization

Skill-gap charts

Resume comparison

Improved mobile responsiveness

Downloadable analysis reports

Architecture Evolution

The current architecture can evolve from:

Django Monolith

into:

                    ┌─────────────────────┐
                    │      Frontend       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      REST API       │
                    │   Django / FastAPI  │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      Resume Service     Matching Service   Interview Service
             │                 │                 │
             └─────────────────┼─────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    PostgreSQL       │
                    └─────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Vector / Embeddings │
                    │  FAISS / ChromaDB   │
                    └─────────────────────┘

This would allow CareerMatch AI to become a larger production-grade career intelligence platform.

Author

Laiba Ashar Malik

Agentic AI Developer

GitHub:
https://github.com/laibaashar642-pixel

Project Status

Current Status: MVP Complete

Core functionality implemented:

Resume PDF processing

Resume analysis

Job description analysis

Skill matching

Semantic similarity

Explainable scoring

Resume audit

Skill evidence

Recommendations

Interview preparation

Professional result dashboard

Next stage:

GitHub
  ↓
Production Configuration
  ↓
Cloud Deployment
  ↓
Live Demo
  ↓
Portfolio / LinkedIn