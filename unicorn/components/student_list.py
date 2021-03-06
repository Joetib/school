from django_unicorn.components import UnicornView
from accounts.models import Student
from django.contrib.auth import get_user, get_user_model
from django.db.models import Q

User = get_user_model()

class StudentListView(UnicornView):
    students = None
    query_string:str = ''

    def mount(self, *args, **kwargs):
        self.get_students()


    def get_students(self, query:str=None):
        self.students = User.objects.filter(is_student=True)
        if self.query_string:
            for query in self.query_string.split(' '):
                self.students = self.students.filter(Q(first_name__icontains=query.strip())| Q(last_name__icontains=query.strip()))
    
    def updated_query_string(self, *args, **kwargs):
        self.get_students()
    
    

