from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.resume_analysis,
        name="resume_analysis",
    ),
]