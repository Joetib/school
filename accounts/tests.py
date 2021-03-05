from django.test import TestCase
from .models import CustomUser
# Create your tests here.
username="username"
password="password"
email="test@email.com"

class TestUser(TestCase):
    def test_create_student(self):
        student = CustomUser.objects.create(username=username, email=email, is_student=True)
        self.assertEqual(student.username, username)
        self.assertEqual(student.email, email)
        self.assertEqual(student.is_student, True)
        self.assertEqual(student.is_teacher, False)
        self.assertEqual(student.is_administrator, False)
    
    def test_create_administrator(self):
        student = CustomUser.objects.create(username=username, email=email, is_administrator=True)
        self.assertEqual(student.username, username)
        self.assertEqual(student.email, email)
        self.assertEqual(student.is_student, False)
        self.assertEqual(student.is_teacher, False)
        self.assertEqual(student.is_administrator, True)
    
    def test_create_teacher(self):
        student = CustomUser.objects.create(username=username, email=email, is_teacher=True)
        self.assertEqual(student.username, username)
        self.assertEqual(student.email, email)
        self.assertEqual(student.is_student, False)
        self.assertEqual(student.is_teacher, True)
        self.assertEqual(student.is_administrator, False)
