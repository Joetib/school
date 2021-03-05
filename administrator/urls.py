from django.urls import path
from . import views

app_name = "administrator"


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('student/create/', views.create_student, name="create-student"),
    path('teacher/create/', views.create_teacher, name="create-teacher"),
]