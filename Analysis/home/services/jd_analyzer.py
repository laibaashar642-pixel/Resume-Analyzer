from .resume_analyzer import find_skills


def analyze_job_description(jd_text):
    skills = find_skills(jd_text)

    return {
        "required_skills": skills,
        "skill_count": len(skills),
        "word_count": len(jd_text.split()),
    }