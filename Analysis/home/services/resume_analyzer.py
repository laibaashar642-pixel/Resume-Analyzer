import re


SKILLS = [
    "python",
    "django",
    "django rest framework",
    "fastapi",
    "flask",
    "sql",
    "postgresql",
    "mysql",
    "oracle",
    "javascript",
    "html",
    "css",
    "react",
    "node.js",
    "c++",
    "c",
    "java",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "computer vision",
    "opencv",
    "mediapipe",
    "yolo",
    "pytorch",
    "tensorflow",
    "numpy",
    "pandas",
    "scikit-learn",
    "langchain",
    "langgraph",
    "rag",
    "llm",
    "embeddings",
    "chromadb",
    "faiss",
    "git",
    "github",
    "docker",
    "rest api",
    "rest apis",
]


def normalize_text(text):
    return re.sub(
        r"\s+",
        " ",
        text.lower()
    ).strip()


def find_skills(text):
    normalized = normalize_text(text)

    found = []

    for skill in SKILLS:
        if skill.lower() in normalized:
            found.append(skill)

    return sorted(set(found))


def extract_email(text):
    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    return match.group(0) if match else None


def extract_phone(text):
    match = re.search(
        r"(?:(?:\+92|0092)[-\s]?)?0?3\d{2}[-\s]?\d{7}",
        text
    )

    return match.group(0) if match else None


def analyze_resume(resume_text):
    skills = find_skills(resume_text)

    return {
        "skills": skills,
        "skill_count": len(skills),
        "email": extract_email(resume_text),
        "phone": extract_phone(resume_text),
        "text_length": len(resume_text),
        "word_count": len(resume_text.split()),
    }
def detect_resume_sections(text):
    normalized = text.lower()

    section_keywords = {
        "summary": [
            "summary",
            "professional summary",
            "profile",
            "objective",
        ],
        "skills": [
            "skills",
            "technical skills",
            "core skills",
        ],
        "experience": [
            "experience",
            "work experience",
            "employment",
        ],
        "projects": [
            "projects",
            "personal projects",
            "academic projects",
        ],
        "education": [
            "education",
            "academic background",
            "qualifications",
        ],
        "certifications": [
            "certifications",
            "certificates",
        ],
    }

    detected = {}

    for section, keywords in section_keywords.items():
        detected[section] = any(
            keyword in normalized
            for keyword in keywords
        )

    return detected


def generate_resume_audit(resume_text):
    sections = detect_resume_sections(resume_text)

    audit = []

    important_sections = [
        "summary",
        "skills",
        "experience",
        "projects",
        "education",
    ]

    for section in important_sections:
        if sections.get(section):
            audit.append({
                "section": section.title(),
                "status": "Present",
                "message": (
                    f"{section.title()} section detected."
                ),
            })
        else:
            audit.append({
                "section": section.title(),
                "status": "Missing",
                "message": (
                    f"Consider adding a {section.title()} "
                    "section if it is relevant to your profile."
                ),
            })

    return audit