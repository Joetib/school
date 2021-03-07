from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username','email', 'get_full_name']

    fieldsets = [
        *UserAdmin.fieldsets,
    ]
    fieldsets.insert(
        2,
        (
            "Profile Information",
            {
                "fields": (
                    #"address",
                    "picture",                    
                    #"phone_number",
                ),
            },
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)