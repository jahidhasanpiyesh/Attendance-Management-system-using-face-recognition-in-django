from django.db import models

# import timezone for handling date and time fields
from django.utils import timezone


# model for student registration
class Student_Registration(models.Model):
    stu_id = models.CharField(
        max_length=30, unique=True, help_text="Unique Id Assigned to Each Student")
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=15)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='student_images/')
    is_active = models.BooleanField(default=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    # string representation of the model instance
    def __str__(self):
        return f"{self.name} ({self.stu_id})"

# model for attendance records


class Attendance(models.Model):
    student_registration = models.ForeignKey(
        Student_Registration, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student_registration.name} - {self.date}"

    # methods to mark check-in and check-out times
    def mark_check_in(self):
        """Mark check-in time for the Students."""
        if not self.check_in_time:
            self.check_in_time = timezone.now()
            self.save()
        else:
            raise ValueError("Check-in time already marked.")

    def mark_check_out(self):
        """Mark check-out time for the Students."""
        if self.check_in_time and not self.check_out_time:
            self.check_out_time = timezone.now()
            self.save()
        else:
            raise ValueError(
                "Cannot mark check-out without check-in or if already checked out.")

    # method to calculate duration spent at class time
    def calculate_duration(self):
        """Calculate the duration the students spent at class."""
        if self.check_in_time and self.check_out_time:
            duration = self.check_out_time - self.check_in_time

            # format duration as hours, minutes, seconds
            hours, remainder = divmod(duration.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)

            # return formatted duration string
            return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
        return "Not yet calculated"

    # override save method to set date automatically at creation
    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            self.date = timezone.now().date()
        super().save(*args, **kwargs)  # call the real save() method

# model for camera configuration


class CameraConfiguration(models.Model):
    name = models.CharField(max_length=100, unique=True,
                            help_text="Give a name to this camera configuration")
    camera_source = models.CharField(
        max_length=255, help_text="Camera index (0 for default webcam or RTSP/HTTP URL for IP camera)")
    threshold = models.FloatField(
        default=0.6, help_text="Face recognition confidence threshold")

    # string representation of the model instance
    def __str__(self):
        return self.name
