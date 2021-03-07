from django_unicorn.components import UnicornView
from accounts.models import Teacher
from django.contrib.auth import get_user, get_user_model
from django.db.models import Q

User = get_user_model()

class TeachersListView(UnicornView):
    teachers = None
    query_string:str = ''

    def mount(self, *args, **kwargs):
        self.get_teachers()


    def get_teachers(self, query:str=None):
        self.teachers = User.objects.filter(is_teacher=True)
        if self.query_string:
            for query in self.query_string.split(' '):
                self.teachers = self.teachers.filter(Q(first_name__icontains=query.strip())| Q(last_name__icontains=query.strip()))
    
    def updated_query_string(self, *args, **kwargs):
        self.get_teachers()
    
    

