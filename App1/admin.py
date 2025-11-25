from django.contrib import admin
from .models import Student_Registration
# Register your models here.


@admin.register(Student_Registration)
class Student_Registration_Admin(admin.ModelAdmin):
    list_display = ('stu_id', 'name', 'email', 'phone_number', 'designation', 'department', 'is_active')
    search_fields = ('stu_id', 'name', 'email', 'department')
    list_filter = ('is_active', 'department', 'designation')
    ordering = ('stu_id',)