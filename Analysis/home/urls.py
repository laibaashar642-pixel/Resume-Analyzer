from django.urls import path,include
from .import views
urlpatterns = [
    path('',views.resume_analysis,name='resume_analysis'),
]