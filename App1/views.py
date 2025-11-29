from django.shortcuts import redirect, render, get_object_or_404
from .models import Student_Registration, CameraConfiguration
from django.contrib import messages
from django.core.files.base import ContentFile
import base64
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
# Create your views here.

# ----------------------------------------Helper function to check if user is admin---------------------------
def is_admin(user):
    return user.is_superuser

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
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

# ----------------------------------------View for logging out the user---------------------------
@login_required
def user_logout(request):
    logout(request)
    return redirect('home')  # logout হলে login page এ redirect

# ----------------------------------------View for rendering the student list page---------------------------
@login_required
@user_passes_test(is_admin)
def stu_list(request):
    students = Student_Registration.objects.all()
    return render(request, 'stu_list.html', {'students': students})

# ----------------------------------------View for authorizing a student---------------------------
@login_required
@user_passes_test(is_admin)
def stu_authorize(request, pk):
    stu = get_object_or_404(Student_Registration, pk=pk)
    
    if request.method == 'POST':
        # Get the 'authorized' checkbox value and update the 'is_active' field
        authorized = request.POST.get('authorized', False)
        stu.is_active = bool(authorized)  # Update the 'is_active' field
        stu.save()
        return redirect('stu_detail', pk=pk)
    
    return render(request, 'stu_authorize.html', {'stu': stu})

# ----------------------------------------View for deleting a student---------------------------
@login_required
@user_passes_test(is_admin)
def stu_delete(request, pk):
    stu = get_object_or_404(Student_Registration, pk=pk)
    
    if request.method == 'POST':
        stu.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('stu_list')  # Redirect to the student list after deletion
    
    return render(request, 'stu_delete.html', {'stu': stu})

# ----------------------------------------View for rendering the student detail page---------------------------
@login_required
@user_passes_test(is_admin)
def stu_detail(request, pk):
    stu = get_object_or_404(Student_Registration, pk=pk)
    return render(request, 'stu_detail.html', {'stu': stu})

# ----------------------------------------View for rendering the attendance list page---------------------------
def attendance_list(request):
    return render(request, 'attendance_list.html')


# ---------------------------------- view for rendering the camera_config_list template page ---------------------------
@login_required
@user_passes_test(is_admin)
def camera_config_create(request):
    # Check if the request method is POST, indicating form submission
    if request.method == "POST":
        # Retrieve form data from the request
        name = request.POST.get('name')
        camera_source = request.POST.get('camera_source')
        threshold = request.POST.get('threshold')

        try:
            # Save the data to the database using the CameraConfiguration model
            CameraConfiguration.objects.create(
                name=name,
                camera_source=camera_source,
                threshold=threshold,
            )
            # Redirect to the list of camera configurations after successful creation
            return redirect('camera_config_list')

        except IntegrityError:
            # Handle the case where a configuration with the same name already exists
            messages.error(request, "A configuration with this name already exists.")
            # Render the form again to allow user to correct the error
            return render(request, 'camera_config_form.html')

    # Render the camera configuration form for GET requests
    return render(request, 'camera_config_form.html')


@login_required
@user_passes_test(is_admin)
def camera_config_list(request):
    # Retrieve all CameraConfiguration objects from the database
    configs = CameraConfiguration.objects.all()
    # Render the list template with the retrieved configurations
    return render(request, 'camera_config_list.html', {'configs': configs})


# UPDATE: Function to edit an existing camera configuration
@login_required
@user_passes_test(is_admin)
def camera_config_update(request, pk):
    # Retrieve the specific configuration by primary key or return a 404 error if not found
    config = get_object_or_404(CameraConfiguration, pk=pk)

    # Check if the request method is POST, indicating form submission
    if request.method == "POST":
        # Update the configuration fields with data from the form
        config.name = request.POST.get('name')
        config.camera_source = request.POST.get('camera_source')
        config.threshold = request.POST.get('threshold')
        config.success_sound_path = request.POST.get('success_sound_path')

        # Save the changes to the database
        config.save()  

        # Redirect to the list page after successful update
        return redirect('camera_config_list')  
    
    # Render the configuration form with the current configuration data for GET requests
    return render(request, 'camera_config_form.html', {'config': config})