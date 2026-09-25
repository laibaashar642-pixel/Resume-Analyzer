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