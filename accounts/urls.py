from django.urls import path
from . import views
app_name = "accounts"

urlpatterns = [
    path('generate-password/', views.generate_password, name="generate-password")
    ]