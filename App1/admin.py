from django.contrib import admin
from .models import Student_Registration, CameraConfiguration
# Register your models here.


@admin.register(Student_Registration)
class Student_Registration_Admin(admin.ModelAdmin):
    list_display = ('stu_id', 'name', 'email', 'phone_number', 'designation', 'department', 'is_active')
    search_fields = ('stu_id', 'name', 'email', 'department')
    list_filter = ('is_active', 'department', 'designation')
    ordering = ('stu_id',)


@admin.register(CameraConfiguration)
class CameraConfigurationAdmin(admin.ModelAdmin):
    list_display = ['name', 'camera_source', 'threshold']
    search_fields = ['name']