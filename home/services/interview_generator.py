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
    for skill in matched[:4]:

        questions.append({
            "question": (
                f"Can you explain your practical "
                f"experience with {skill} and describe "
                f"a project where you used it?"
            ),
            "why": (
                f"{skill} was detected as a skill that "
                "matches this job requirement."
            ),
            "prepare": (
                f"Prepare one real project example "
                f"where you used {skill}, including "
                "what you built and your contribution."
            ),
        })

    # Questions based on missing skills
    for skill in missing[:3]:

        questions.append({
            "question": (
                f"What do you know about {skill}, "
                "and how would you apply it in this role?"
            ),
            "why": (
                f"{skill} appears in the job description "
                "but was not detected in your resume."
            ),
            "prepare": (
                f"Review the fundamentals of {skill} "
                "and understand its common use cases."
            ),
        })

    # General backend question
    questions.append({
        "question": (
            "How would you design a REST API for "
            "an AI-powered application?"
        ),
        "why": (
            "The role involves backend development "
            "and REST API design."
        ),
        "prepare": (
            "Review API endpoints, HTTP methods, "
            "status codes, authentication, validation, "
            "and Django REST Framework or FastAPI."
        ),
    })

    # Debugging question
    questions.append({
        "question": (
            "How do you debug a backend application "
            "when an API returns unexpected results?"
        ),
        "why": (
            "Backend developers are expected to "
            "identify and resolve API problems."
        ),
        "prepare": (
            "Review logging, request/response inspection, "
            "validation, database queries, exceptions, "
            "and debugging techniques."
        ),
    })

    # Project question
    questions.append({
        "question": (
            "Walk me through your most relevant project "
            "for this position."
        ),
        "why": (
            "Interviewers commonly use projects to "
            "evaluate practical experience."
        ),
        "prepare": (
            "Prepare a clear explanation of the project "
            "problem, architecture, technologies, "
            "your contribution, and outcome."
        ),
    })

    # Scalability question
    questions.append({
        "question": (
            "How would you improve the scalability "
            "and maintainability of a Python backend?"
        ),
        "why": (
            "The role requires building maintainable "
            "and scalable backend applications."
        ),
        "prepare": (
            "Review modular architecture, database "
            "optimization, caching, asynchronous "
            "processing, API design, and clean code."
        ),
    })

    return questions[:10]