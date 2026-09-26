from django.shortcuts import render

from .forms import ResumeAnalysisForm

from .services.pdf_parser import (
    extract_text_from_pdf,
)

from .services.resume_analyzer import (
    analyze_resume,
    generate_resume_audit,
)

from .services.jd_analyzer import (
    analyze_job_description,
)

from .services.matcher import (
    calculate_match,
    generate_recommendations,
    generate_match_explanation,
)

from .services.interview_generator import (
    generate_interview_questions,
)


def resume_analysis(request):

    if request.method == "POST":

        form = ResumeAnalysisForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            try:

                # 1. Get uploaded resume
                resume_file = form.cleaned_data[
                    "resume"
                ]

                job_description = form.cleaned_data[
                    "job_description"
                ]

                # 2. Extract PDF text
                resume_text = extract_text_from_pdf(
                    resume_file
                )

                # 3. Analyze resume
                resume_data = analyze_resume(
                    resume_text
                )

                # 4. Resume quality audit
                resume_audit = generate_resume_audit(
                    resume_text
                )

                # 5. Analyze job description
                jd_data = analyze_job_description(
                    job_description
                )

                # 6. Calculate skill + semantic match
                match_data = calculate_match(
                    resume_data,
                    jd_data,
                    resume_text,
                    job_description,
                )

                # 7. Explain why the score was generated
                match_explanation = (
                    generate_match_explanation(
                        match_data
                    )
                )

                # 8. Generate recommendations
                recommendations = (
                    generate_recommendations(
                        match_data
                    )
                )

                # 9. Generate interview questions
                interview_questions = (
                    generate_interview_questions(
                        resume_data,
                        jd_data,
                        match_data,
                    )
                )

                # 10. Send everything to result page
                context = {
                    "resume_data": resume_data,
                    "resume_audit": resume_audit,
                    "jd_data": jd_data,
                    "match_data": match_data,
                    "match_explanation": (
                        match_explanation
                    ),
                    "recommendations": (
                        recommendations
                    ),
                    "interview_questions": (
                        interview_questions
                    ),
                }

                return render(
                    request,
                    "home/result.html",
                    context,
                )

            except ValueError as exc:

                form.add_error(
                    None,
                    str(exc),
                )

        return render(
            request,
            "home/upload.html",
            {"form": form},
        )

    # GET request
    form = ResumeAnalysisForm()

    return render(
        request,
        "home/upload.html",
        {"form": form},
    )