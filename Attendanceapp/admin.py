from django.contrib import admin
from .models import Student
# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'student_id', 
        'name', 
        'email', 
        'phone_number', 
        'section', 
        'department', 
        'is_active'
    ]
    list_filter = ['department', 'is_active']
    search_fields = ['name', 'email', 'student_id']
    ordering = ['student_id']  # Orders by Student ID