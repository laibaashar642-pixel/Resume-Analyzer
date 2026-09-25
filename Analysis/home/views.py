from django.shortcuts import render

from .forms import ResumeAnalysisForm
from .services.pdf_parser import extract_text_from_pdf
from .services.resume_analyzer import analyze_resume
from .services.jd_analyzer import analyze_job_description
from .services.matcher import (
    calculate_match,
    generate_recommendations,
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

                resume_file = form.cleaned_data[
                    "resume"
                ]

                job_description = (
                    form.cleaned_data[
                        "job_description"
                    ]
                )

                # 1. Extract PDF text
                resume_text = extract_text_from_pdf(
                    resume_file
                )

                # 2. Resume analysis
                resume_data = analyze_resume(
                    resume_text
                )

                # 3. JD analysis
                jd_data = analyze_job_description(
                    job_description
                )

                # 4. Semantic + skill matching
                match_data = calculate_match(
                    resume_data,
                    jd_data,
                    resume_text,
                    job_description,
                )

                # 5. Recommendations
                recommendations = (
                    generate_recommendations(
                        match_data
                    )
                )

                # 6. Interview questions
                interview_questions = (
                    generate_interview_questions(
                        resume_data,
                        jd_data,
                        match_data,
                    )
                )

                context = {
                    "resume_data": resume_data,
                    "jd_data": jd_data,
                    "match_data": match_data,
                    "recommendations": recommendations,
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

    form = ResumeAnalysisForm()

    return render(
        request,
        "home/upload.html",
        {"form": form},
    )