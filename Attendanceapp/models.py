from django.db import models

# Create your models here.
class Student(models.Model):
    student_id = models.CharField(
        max_length=50, unique=True, help_text="Unique ID assigned to the Student"
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=15)
    section = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to="students/", blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.student_id})"