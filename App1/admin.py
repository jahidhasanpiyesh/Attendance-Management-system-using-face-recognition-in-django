from django.contrib import admin
from .models import Student_Registration, CameraConfiguration, Attendance
# Register your models here.


@admin.register(Student_Registration)
class Student_Registration_Admin(admin.ModelAdmin):
    list_display = ('stu_id', 'name', 'email', 'phone_number', 'designation', 'department', 'is_active')
    search_fields = ('stu_id', 'name', 'email', 'department')
    list_filter = ('is_active', 'department', 'designation')
    ordering = ('stu_id',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student_registration', 'date', 'check_in_time', 'check_out_time']
    list_filter = ['date']
    search_fields = ['student_registration__name', 'student_registration__stu_id']

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return ['student_registration', 'date', 'check_in_time', 'check_out_time']
        return ['date', 'check_in_time', 'check_out_time']  # Adding a new object

    def save_model(self, request, obj, form, change):
        if change:  # Editing an existing object
            # Ensure check-in and check-out times cannot be modified via admin
            original = Attendance.objects.get(id=obj.id)
            obj.check_in_time = original.check_in_time
            obj.check_out_time = original.check_out_time
        super().save_model(request, obj, form, change)

@admin.register(CameraConfiguration)
class CameraConfigurationAdmin(admin.ModelAdmin):
    list_display = ['name', 'camera_source', 'threshold']
    search_fields = ['name']