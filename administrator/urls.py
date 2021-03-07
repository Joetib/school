from django.urls import path
from . import views

app_name = "administrator"


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path("students/", views.StudentListView.as_view(), name="student-list"),
    path('students/create/', views.create_student, name="create-student"),
    path('teachers/', views.TeacherListView.as_view(), name="teacher-list"),
    path('teachers/create/', views.create_teacher, name="create-teacher"),
    path('classes/create/', views.create_klass, name="create-class"),
]