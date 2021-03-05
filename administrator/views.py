from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import administrator_required
from . import forms
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()

@login_required
@administrator_required
def dashboard(request):

    return render(request, 'administrator/dashboard.html', {
        'teachers': User.objects.filter(is_teacher=True),
        'students': User.objects.filter(is_student=True),
    })

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
