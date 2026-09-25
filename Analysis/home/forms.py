from django import forms


class ResumeAnalysisForm(forms.Form):

    resume = forms.FileField(
        label="Resume PDF",
        widget=forms.ClearableFileInput(
            attrs={
                "accept": ".pdf",
            }
        )
    )

    job_description = forms.CharField(
        label="Job Description",
        widget=forms.Textarea(
            attrs={
                "rows": 12,
                "placeholder": (
                    "Paste the job description here..."
                ),
            }
        )
    )

    def clean_resume(self):
        resume = self.cleaned_data["resume"]

        if not resume.name.lower().endswith(".pdf"):
            raise forms.ValidationError(
                "Please upload a PDF file."
            )

        if resume.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                "Resume must be smaller than 5 MB."
            )

        return resume