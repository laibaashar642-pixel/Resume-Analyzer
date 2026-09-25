from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_semantic_similarity(resume_text, jd_text):
    resume_embedding = model.encode(
        [resume_text],
        normalize_embeddings=True,
    )

    jd_embedding = model.encode(
        [jd_text],
        normalize_embeddings=True,
    )

    similarity = cosine_similarity(
        resume_embedding,
        jd_embedding,
    )[0][0]

    similarity = max(0, min(1, similarity))

    return round(similarity * 100)


def find_skill_evidence(skill, resume_text):
    """
    Find the sentence/line from the resume
    where the skill appears.
    """

    lines = resume_text.splitlines()

    skill_lower = skill.lower()

    for line in lines:
        if skill_lower in line.lower():
            return line.strip()

    # Try word-based matching for things like REST API
    normalized_skill = skill_lower.replace("-", " ")

    for line in lines:
        normalized_line = line.lower().replace("-", " ")

        if normalized_skill in normalized_line:
            return line.strip()

    return None


def calculate_match(
    resume_data,
    jd_data,
    resume_text="",
    jd_text="",
):

    resume_skills = set(
        resume_data.get("skills", [])
    )

    required_skills = set(
        jd_data.get("required_skills", [])
    )

    if required_skills:

        matched = sorted(
            resume_skills.intersection(
                required_skills
            )
        )

        missing = sorted(
            required_skills.difference(
                resume_skills
            )
        )

        skill_score = round(
            (len(matched) / len(required_skills))
            * 100
        )

    else:

        matched = []
        missing = []
        skill_score = 0

    semantic_score = 0

    if resume_text and jd_text:

        semantic_score = calculate_semantic_similarity(
            resume_text,
            jd_text,
        )

    final_score = round(
        (skill_score * 0.60)
        + (semantic_score * 0.40)
    )

    # Evidence
    evidence = []

    for skill in matched:

        evidence_text = find_skill_evidence(
            skill,
            resume_text,
        )

        evidence.append({
            "skill": skill,
            "evidence": evidence_text
            or "Skill detected in resume.",
        })

    return {
        "score": final_score,
        "skill_score": skill_score,
        "semantic_score": semantic_score,
        "match_percentage": final_score,

        "matched_skills": matched,
        "missing_skills": missing,

        "required_skills": sorted(
            required_skills
        ),

        "evidence": evidence,
    }


def generate_recommendations(match_data):

    recommendations = []

    missing = match_data.get(
        "missing_skills",
        []
    )

    semantic_score = match_data.get(
        "semantic_score",
        0
    )

    if missing:

        recommendations.append(
            "Strengthen the missing technical skills "
            "identified from the job description."
        )

        for skill in missing[:5]:

            recommendations.append(
                f"Consider learning or strengthening "
                f"{skill}."
            )

    if semantic_score < 50:

        recommendations.append(
            "Tailor your resume more closely to "
            "the responsibilities and terminology "
            "of this role."
        )

    elif semantic_score >= 75:

        recommendations.append(
            "Your resume has strong semantic relevance "
            "to this job description."
        )

    if not recommendations:

        recommendations.append(
            "Your resume has reasonable alignment "
            "with the detected job requirements."
        )

    return recommendations