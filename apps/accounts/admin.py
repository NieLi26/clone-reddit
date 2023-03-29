from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'username',
        'date_of_birth',
        'thumbnail',
        'date_joined'
    ]
    fieldsets = UserAdmin.fieldsets + (
        ('Extra', {
            'classes': ('wide',),
            'fields': ('thumbnail',),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra', {
            'classes': ('wide',),
            'fields': ('thumbnail',),
        }),
    )
    # raw_id_fields = ['user'] fk or m2m
