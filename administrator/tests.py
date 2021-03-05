from django.test import TestCase
from http import HTTPStatus
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your tests here.
password = 'thepasskeywornd!'
username = 'administrator'
email = 'administrator@email.com'
class TestAdministrator(TestCase):
    def test_dashboard(self):
        response = self.client.get('/administrator/')
        # should get redirected to the login view
        self.assertEqual(response.status_code, 302)     # replace with appropriate status_code name.   
    def test_student_access_administrator_dashboard(self):
        student = User.create_student(username=username, email=email, password=password)
        self.assertEqual(student.is_student, True)
        self.client.login(username=username, email=email, password=password)
        response = self.client.get('/administrator/')
        self.assertEqual(response.status_code, 400)

    def test_teacher_access_administrator_dashboard(self):
        teacher = User.create_teacher(username=username, email=email, password=password)
        self.assertEqual(teacher.is_teacher, True)
        self.client.login(username=username, email=email, password=password)
        response = self.client.get('/administrator/')
        self.assertEqual(response.status_code, 400)
    
    def test_administrator_access_administrator_dashboard(self):
        administrator = User.create_administrator(username=username, email=email, password=password)
        self.assertEqual(administrator.is_administrator, True)
        self.client.login(username=username, email=email, password=password)
        response = self.client.get('/administrator/')
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_create_user_get(self):
        administrator = User.create_administrator(username=username, email=email, password=password)
        self.assertEqual(administrator.is_administrator, True)
        self.client.login(username=username, email=email, password=password)
        response = self.client.get('/administrator/student/create/')
        
        self.assertEqual(response.status_code, 200)
        
    
    
    
        
