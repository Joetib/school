from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse

# Create your views here.


import secrets

def generate_password(request: HttpRequest) -> HttpResponse:
    password = secrets.token_urlsafe(10)
    return JsonResponse({'success': True, 'password': password})