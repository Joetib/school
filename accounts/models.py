from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    picture = models.ImageField(upload_to="profile/", blank=True, null=True)
    date_of_birth = models.DateField()


    # True only for administrators
    is_administrator = models.BooleanField(default=False)
    # True only for accountants
    is_accountant = models.BooleanField(default=False)
    # True only for teachers
    is_teacher = models.BooleanField(default=False)
    # True only for students
    is_student = models.BooleanField(default=False)

    def get_active_class(self):
        try:
            if self.is_student:
                return self.student_profile.klasses.filter(is_active=True).first()
        except:
            return None
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
        return self.get_full_name()


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
        return self.user.get_full_name()


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="student_profile")
    start_date = models.DateTimeField(default=timezone.now)
    is_active= models.BooleanField(default=True)
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ("is_active", "-start_date")
    
    def __str__(self):
        return self.user.get_full_name()



class Klass(models.Model):
    CLASS_CHOICES=(
        ('stage 1', "Primary One"),
        ("stage 2", "Primary Two"),
        ("stage 3", "Primary Three"),
        ("stage 4", "Primary Four"),
        ("stage 5", "Primary Five"),
        ("stage 6", "Primary Six"),
        ('jhs 1', "Junior High 1"),
        ('jhs 2', "Junior High 2"),
        ('jhs 3', "Junior High 3"),
    )
    klass_name = models.CharField(choices=CLASS_CHOICES, max_length=10)
    is_active = models.BooleanField(default=True)
    start_year = models.DateField(default=timezone.now)
    end_year = models.DateField(blank=True, null=True)
    teachers = models.ManyToManyField(Teacher, related_name="teachers", symmetrical=True)
    students = models.ManyToManyField(Student, related_name="klasses", symmetrical=True)

    
    class Meta:
        unique_together = ('is_active',  'klass_name')
        ordering = ("-is_active", "klass_name")
    
    def save(self, *args, **kwargs):
        if not self.pk:
            if self.is_active:
                Klass.objects.filter(is_active=True, klass_name=self.klass_name).update(is_active=False, end_year=timezone.now().date())
        super().save(*args, **kwargs)

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


@receiver(post_save, sender=CustomUser)
def create_related_profile(sender, instance, created=False, **kwargs):
    """
    create a new product notification for all followers of a shop
    """
    if instance.is_student:
        Student.objects.get_or_create(user=instance)
    elif instance.is_teacher:
        Teacher.objects.get_or_create(user=instance)
