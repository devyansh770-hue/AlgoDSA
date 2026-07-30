from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'preferred_language', 'streak', 'solved_count', 'is_staff')
    list_filter = ('preferred_language', 'is_staff', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('DSA Profile', {
            'fields': ('bio', 'preferred_language', 'streak', 'longest_streak',
                       'solved_count', 'last_active_date', 'avatar_url')
        }),
    )
