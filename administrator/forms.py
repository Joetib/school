from django import forms
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row

# Get the authentication class
User = get_user_model()


class StudentCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

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

    def save(self, *args, **kwargs):
        student = super(StudentCreateForm, self).save(*args, **kwargs)
        student.set_password(self.cleaned_data['password'])
        student.is_student = True
        student.save()
        return student

class TeacherCreateForm(StudentCreateForm):
    def save(self, *args, **kwargs):

        teacher = super(TeacherCreateForm, self).save(*args, **kwargs)
        teacher.set_password(self.cleaned_data['password'])
        teacher.is_teacher = True
        teacher.save()
        return teacher