import base64
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student
from django.core.files.base import ContentFile

# Create your views here.
def home(request):
    return render(request, 'home.html')

def register_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        student_id = request.POST.get('student_id')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        section = request.POST.get('section')
        department = request.POST.get('department')
        image_data = request.POST.get('image_data')

        # Check for duplicate employee ID
        if Student.objects.filter(student_id=student_id).exists():
            messages.error(request, "An student with this ID already exists.")
            return render(request, 'register_student.html')

        # Decode the base64 image data
        profile_picture = None
        if image_data:
            try:
                header, encoded = image_data.split(',', 1)
                profile_picture = ContentFile(base64.b64decode(encoded), name=f"{student_id}.jpg")
            except Exception as e:
                messages.error(request, "Error decoding image. Please try again.")
                print(f"Error decoding image: {e}")
                return render(request, 'register_employee.html')

        # Create the Student instance
        student = Student(
            student_id=student_id,
            name=name,
            email=email,
            phone_number=phone_number,
            section=section,
            department=department,
            profile_picture=profile_picture,  # Use profile_picture field
            is_active=True  # Default to True, or customize as needed
        )

        # Save the Student and redirect to a success page
        try:
            student.save()
            messages.success(request, "Student registered successfully.")
            return redirect('register_success')  # Redirect to a success page (customize as needed)
        except Exception as e:
            messages.error(request, "An error occurred while registering the Student. Please try again.")
            print(f"Error saving Student: {e}")
            return render(request, 'register_student.html')

    return render(request, 'register_student.html')