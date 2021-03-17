from accounts.models import AcademicYear, Klass
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import administrator_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from . import forms
from django.views.generic import ListView, TemplateView, CreateView, DetailView
from django.contrib.auth import get_user_model

from accounts.models import Student, Teacher, Course, NoticeBoard
from datetime import datetime
# Create your views here.

User = get_user_model()

@login_required
@administrator_required
def dashboard(request):
    return render(request, 'administrator/dashboard.html', {
        'teachers': User.objects.filter(is_teacher=True),
        'students': User.objects.filter(is_student=True),
        'notices': NoticeBoard.objects.all(),
    })

class StudentListView(TemplateView):
    template_name = "administrator/student_list.html"

class TeacherListView(TemplateView):
    template_name = "administrator/teacher_list.html"

@login_required
@administrator_required
def create_student(request):
    if request.method == "POST":
        student_form = forms.StudentCreateForm(request.POST, files=request.FILES)
        if student_form.is_valid():
            student = student_form.save()
            messages.success(request, f'Student: {student.username} created successfully')
            return redirect("administrator:dashboard")
        messages.error(request, "Unable to create student, please try again")
    else:
        student_form = forms.StudentCreateForm()
    return render(request, 'administrator/create_student.html', {'student_form': student_form})

@login_required
@administrator_required
def create_teacher(request):
    if request.method == "POST":
        teacher_form = forms.TeacherCreateForm(request.POST, files=request.FILES)
        if teacher_form.is_valid():
            teacher = teacher_form.save()
            messages.success(request, f'Student: {teacher.username} created successfully')
            return redirect("administrator:dashboard")
        messages.error(request, "Unable to create teacher, please try again")
    else:
        teacher_form = forms.TeacherCreateForm()
    return render(request, 'administrator/create_teacher.html', {'teacher_form': teacher_form})

@login_required
@administrator_required
def student_profile(request, id):
    student = get_object_or_404(Student, user__id=id)
    age = int((datetime.now().date() - student.user.date_of_birth).days / 365 )
    return render(request, 'administrator/student_profile.html', {'student':student,'age':age,})

@login_required
@administrator_required
def teacher_profile(request, id):
    teacher = get_object_or_404(Teacher, user__id=id)
    age = int((datetime.now().date() - teacher.user.date_of_birth).days / 365 )
    return render(request, 'administrator/teacher_profile.html', {'teacher':teacher,'age':age})

def create_academic_year(request: HttpRequest):
    if request.method == "POST":
        academic_year_form = forms.AcademicYearForm(request.POST)
        if academic_year_form.is_valid():
            academic_year = academic_year_form.save()
            return redirect(academic_year.get_admin_absolute_url())
    else:
        academic_year_form = forms.AcademicYearForm()
    return render(request, "administrator/create_academic_year.html", {'form': academic_year_form})
""" class SubjectList(ListView):
    model = Course
    template_name = 'administration/subject_list.html'
    context_object_name = 'subjects' """

class AcademicYearListView(ListView):
    model = AcademicYear
    context_object_name = "academic_years"
    template_name = "administrator/academic_year_list.html"


class AcademicYearDetailView(DetailView):
    model = AcademicYear
    context_object_name = "academic_year"
    template_name = "administrator/academic_year_detail.html"



def create_klass(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    if request.method == "POST":
        form = forms.KlassCreateForm(request.POST, files=request.FILES)
        if form.is_valid():
            klass = form.save()
            return redirect("administrator:dashboard")
        else:
            print("Form is invalid\n\n\n\n")
            print(form.errors)
    else:
        form = forms.KlassCreateForm()
    return render(request, 'administrator/create_class.html', {'form': form})

class KlassListview(ListView):
    model = Klass
    template_name = "administrator/class_list.html"
    context_object_name = "classes"

    def qet_queryset(self, *args, **kwargs):
        return Klass.objects.filter(academic_year__is_active=True)

class KlassDetailView(DetailView):
    model = Klass
    template_name = "administrator/klass_detail.html"
    context_object_name = "klass"

def add_students_to_class(request: HttpRequest, pk:int):
    klass = get_object_or_404(Klass, pk=pk, academic_year__is_active=True)
    if request.method == "POST":
        students_form = forms.AddStudentToClassForm(request.POST, klass=klass)
        if students_form.is_valid():
            cd = students_form.cleaned_data
            # TODO: this is too slow O(n)
            for student in cd['students']:
                student.klasses.add(klass)
            # a faster version is 
            # klass.students.add(*cd['students'])
            # but it keeps raising contraint errors.

            return redirect(klass.get_admin_absolute_url())
    else:
        students_form = forms.AddStudentToClassForm(klass=klass)
    return render(request, "administrator/add_student_to_class.html", {'form': students_form, 'klass': klass})

@administrator_required
def add_teachers_to_class(request: HttpRequest, pk:int):
    klass = get_object_or_404(Klass, pk=pk, academic_year__is_active=True)
    if request.method == "POST":
        teacher_form = forms.AddTeacherToClassForm(request.POST, instance=klass)
        
        if teacher_form.is_valid():
            teacher_form.save()

            return redirect(klass.get_admin_absolute_url())
    else:
        teacher_form = forms.AddTeacherToClassForm(instance=klass)
    return render(request, "administrator/add_teacher_to_class.html", {'form': teacher_form, 'klass': klass})
    
def create_course(request):
    if request.method == "POST":
        form = forms.CourseCreateForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("administrator:dashboard")
    else:
        form = forms.CourseCreateForm()
    return render(request, 'administrator/create_course.html', {'form': form})


class CoursetListView(ListView):
    model = Course
    template_name = 'administrator/course_list.html'
    context_object_name = 'courses'

    def get_queryset(self, *args, **kwargs):
        return Course.objects.all()


def create_notice(request):
    if request.method == "POST":
        form = forms.CreateNoticeForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("administrator:dashboard")
    else:
        form = forms.CreateNoticeForm()
    return render(request, 'administrator/create_notice.html', {'form':form})

def delete_notice_item(request, id):
    notice = get_object_or_404(NoticeBoard, id=id)
    notice.delete()
    return redirect("administrator:dashboard")
