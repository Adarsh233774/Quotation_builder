from django.urls import path
from . import views

urlpatterns = [
    path('projects/create/', views.project_create, name='project_create'),
]
