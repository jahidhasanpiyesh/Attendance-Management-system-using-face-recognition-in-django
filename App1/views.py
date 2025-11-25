from django.shortcuts import redirect, render
from .models import Student_Registration
from django.contrib import messages
from django.core.files.base import ContentFile
import base64
# Create your views here.

# ----------------------------------------View for rendering the home page---------------------------
def home(request):
    return render(request, 'index.html')

# --------------------------------------View for rendering the student registration page---------------------------
def register_stu(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        stu_id = request.POST.get('stu_id')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        designation = request.POST.get('designation')
        department = request.POST.get('department')
        image_data = request.POST.get('image_data')

        # Decode the base64 image data
        profile_image = None
        if image_data:
            try:
                header, encoded = image_data.split(',', 1)
                profile_image = ContentFile(base64.b64decode(encoded), name=f"{stu_id}.jpg")
            except Exception as e:
                messages.error(request, "Error processing profile image. please try again!")
                print(f"Error decoding image: {e}")
                return render(request, 'register_stu.html')


        student_registration = Student_Registration(
            stu_id=stu_id,
            name=name,
            email=email,
            phone_number=phone_number,
            designation=designation,
            department=department,
            profile_image=profile_image,
            is_active = True
        )
        
        # Save the student registration data to the database
        try:
            student_registration.save()
            messages.success(request, "Student Registered Successfully")
            return redirect('register_success')
        except Exception as e:
            messages.error(request, "Error saving student registration. Please try again.")
            print(f"Error saving student registration: {e}")
            return render(request, 'register_stu.html')
        
    return render(request, 'register_stu.html')

# ----------------------------------------View for rendering the registration success page---------------------------
def register_success(request):
    return render(request, 'register_success.html')

# ----------------------------------------View for rendering the login page---------------------------
def login(request):
    return render(request, 'login.html')

# ----------------------------------------View for rendering the student list page---------------------------
def stu_list(request):
    return render(request, 'stu_list.html')

# ----------------------------------------View for rendering the attendance list page---------------------------
def attendance_list(request):
    return render(request, 'attendance_list.html')