from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    picture = models.ImageField(upload_to="profile/", blank=True, null=True)


    # True only for administrators
    is_administrator = models.BooleanField(default=False)
    # True only for accountants
    is_accountant = models.BooleanField(default=False)
    # True only for teachers
    is_teacher = models.BooleanField(default=False)
    # True only for students
    is_student = models.BooleanField(default=False)

    @classmethod
    def create_administrator(cls,  password, email,username=None, picture=None, **kwargs):
        """
        Creates a new Administrator object with the details provided above.
        It automatically sets the `is_administrator` property of the user created to True
        """
        if not username:
            username = email.split('@')[0]

        user = cls.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()
        return user

    @classmethod
    def create_teacher(cls, password, email,  username=None, picture=None, **kwargs):
        """
        Creates a new Teacher object with the details provided above.
        It automatically sets the `is_teacher` property of the user created to True
        """
        if not username:
            username = email.split('@')[0]
        user = cls.objects.create(username=username, email=email, picture=picture, is_teacher=True, **kwargs )
        user.set_password(password)
        user.save()
        return user

    @classmethod
    def create_student(cls,  password, email, picture=None, username=None, **kwargs):
        """
        Creates a new Student object with the details provided above.
        It automatically sets the `is_student` property of the user created to True
        """
        if not username:
            username = email.split('@')[0]
        user = cls.objects.create(username=username, email=email, picture=picture, is_student=True, **kwargs)
        user.set_password(password)
        user.save()
        return user

    

    def __str__(self):
        return self.full_name


class EducationalBackground(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="educational_backgrounds")
    institution = models.CharField(max_length=500)
    certification = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.certification} at {self.institution}"

class Address(models.Model):
    """
    Address for a person
    A person can have multiple addresses.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="addresses")
    region = models.CharField(max_length=100)
    town = models.CharField(max_length=200)
    location = models.TextField()
    is_active = models.BooleanField(default=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_ended = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        if self.pk and not self.is_active:
            if Address.objects.get(self.pk).is_active:
                self.date_ended = timezone.now()
        super().save(*args, **kwargs)



class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="teacher_profile")
    
    is_active=models.BooleanField(default=True)
    class Meta:
        unique_together = ('user',)

    def __str__(self):
        return self.user.full_name


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="student_profile")
    start_date = models.DateTimeField(default=timezone.now)
    is_active= models.BooleanField(default=True)
    end_date = models.DateTimeField()

    class Meta:
        ordering = ("is_active", "-start_date")
    
    def __str__(self):
        return self.user.full_name



class Klass(models.Model):
    CLASS_CHOICES=(
        ('p1', "Primary One"),
        ("p2", "Primary Two"),
        ("p3", "Primary Three"),
        ("p4", "Primary Four"),
        ("p5", "Primary Five"),
        ("p6", "Primary Six"),
        ('j1', "Junior High 1"),
        ('j2', "Junior High 2"),
        ('j3', "Junior High 3"),
    )
    klass_name = models.CharField(choices=CLASS_CHOICES, max_length=2)
    is_active = models.BooleanField()
    start_year = models.DateField()
    end_year = models.DateField()
    students = models.ManyToManyField(Student, related_name="klasses")

    
    class Meta:
        unique_together = ('is_active', 'klass_name')
        ordering = ("is_active", "klass_name")
    
    def __str__(self):
        return self.klass_name

class Course(models.Model):
    klass = models.ForeignKey(Klass, related_name="courses", on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(Teacher, related_name="assigned_courses", on_delete=models.SET_NULL, blank=True, null=True)
    students = models.ManyToManyField(Student, related_name="registered_courses", blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('klass', 'name', 'is_active')
