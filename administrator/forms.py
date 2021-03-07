from accounts.models import Klass
from django import forms
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row

# Get the authentication class
User = get_user_model()


class StudentCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "picture",
            "date_of_birth",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column(
                Row(
                    Column("username", css_class="col-sm-6 col-md-4"),
                    Column("email", css_class="col-sm-6 col-md-4"),
                    Column("password", css_class="col-sm-12 col-md-4"),
                ),
                css_class="shadow my-3 p-3",
            ),
            Column(
                Row(
                    Column("first_name", css_class="col-sm-6"),
                    Column("last_name", css_class="col-sm-6"),
                    Column("date_of_birth", css_class="col-12"),
                ),
                css_class="shadow p-3 my-3",
            ),
            Column("picture", css_class="shadow py-3 my-3"),
        )
        self.helper.form_tag = False

    def save(self,is_student=True, commit=True, *args, **kwargs):
        student = super(StudentCreateForm, self).save(commit=False*args, **kwargs)
        student.set_password(self.cleaned_data["password"])
        if is_student:
            student.is_student = True
            if commit:
                student.save()
        return student


class TeacherCreateForm(StudentCreateForm):
    def save(self, commit=True, *args, **kwargs):

        teacher = super(TeacherCreateForm, self).save(is_student=False, commit=False, *args, **kwargs)
        teacher.is_teacher = True
        if commit:
            teacher.save()
        return teacher


class KlassCreateForm(forms.ModelForm):
    start_year = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    end_year = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Klass
        fields = ("klass_name", "is_active", "start_year", "end_year")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column("klass_name"),
            Column("is_active"),
            Column(
                Row(
                    Column("start_year", css_class="col-sm-6"),
                    Column("end_year", css_class="col-sm-6 "),
                ),
            ),
        )
        self.helper.form_tag = False
