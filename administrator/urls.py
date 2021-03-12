from django.urls import path
from . import views

app_name = "administrator"


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path("students/", views.StudentListView.as_view(), name="student-list"),
    path('students/create/', views.create_student, name="create-student"),
    path('teachers/', views.TeacherListView.as_view(), name="teacher-list"),
    path('teachers/create/', views.create_teacher, name="create-teacher"),
    path('student/<int:id>/profile/', views.student_profile, name="student-profile"),
    path('teacher/<int:id>/profile/', views.teacher_profile, name="teacher-profile"),
    path('classes/create/', views.create_klass, name="create-class"),
    path('classes/list/', views.KlassListview.as_view(), name="class-list"),
    path('classes/list/<int:pk>', views.KlassDetailView.as_view(), name="class-detail"),
    path('classes/list/<int:pk>/add-students/', views.add_students_to_class, name="add-students-to-class"),
    path('academic-year/', views.AcademicYearListView.as_view(), name="academic-year-list"),
    path('academic-year/create/', views.create_academic_year, name="create-academic-year"),
    path('academic-year/<int:pk>/', views.AcademicYearDetailView.as_view(), name="academic-year-detail"),
    path('course/create/', views.create_course, name="create-course"),
    path('couerse/list/', views.CoursetListView.as_view(), name="course-list"),
    path('notice/create/', views.create_notice, name="create-notice"),
    path('notice/delete/<int:id>/', views.delete_notice_item, name="delete-notice-item"),

]