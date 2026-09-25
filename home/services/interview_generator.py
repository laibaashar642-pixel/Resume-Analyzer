def generate_interview_questions(
    resume_data,
    jd_data,
    match_data,
):

    questions = []

    matched = match_data.get(
        "matched_skills",
        []
    )

    missing = match_data.get(
        "missing_skills",
        []
    )

    # Questions based on matched skills
    for skill in matched[:5]:

        questions.append(
            f"Can you explain your practical experience "
            f"with {skill} and describe a project where "
            f"you used it?"
        )

    # Questions based on missing skills
    for skill in missing[:4]:

        questions.append(
            f"What do you know about {skill}, and how "
            f"would you apply it in this role?"
        )

    # Role-specific questions
    questions.extend([
        "Walk me through your most relevant project "
        "for this position.",

        "How would you design a REST API for an "
        "AI-powered application?",

        "How do you debug a backend application when "
        "an API is returning unexpected results?",

        "How would you improve the scalability and "
        "maintainability of a Python backend?",
    ])

    # Remove duplicates while preserving order
    unique_questions = []

    for question in questions:

        if question not in unique_questions:
            unique_questions.append(question)

    return unique_questions[:10]