# Import necessary Django modules and models
from django.shortcuts import redirect, render, get_object_or_404
from .models import Student_Registration, CameraConfiguration, Attendance
from django.contrib import messages
from django.core.files.base import ContentFile
import base64
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.conf import settings
from django.utils.timezone import now
from facenet_pytorch import InceptionResnetV1, MTCNN

# Import necessary libraries
import os
import cv2
import numpy as np
import pygame
import torch
import mtcnn
import threading
import time


# Initialize MTCNN and InceptionResnetV1
mtcnn = MTCNN(keep_all=True)
# Set to evaluation mode
resnet = InceptionResnetV1(pretrained='vggface2').eval()


# ============================================= Function to detect and encode faces ====================================
def detect_and_encode(image):
    with torch.no_grad():  # disable gradient calculation for inference
        boxes, _ = mtcnn.detect(image)
        if boxes is not None:
            faces = []
            for box in boxes:
                face = image[int(box[1]):int(box[3]), int(
                    box[0]):int(box[2])]   # Crop the face
                if face.size == 0:
                    continue
                face = cv2.resize(face, (160, 160))         # Resize to 160*160
                face = np.transpose(face, (2, 0, 1)).astype(
                    np.float32) / 255.0  # Normalize the face
                face_tensor = torch.tensor(face).unsqueeze(0)
                encoding = resnet(face_tensor).detach().numpy().flatten()
                faces.append(encoding)
            return faces
    return []


# Function to encode uploaded images
def encode_uploaded_images():
    known_face_encodings = []
    known_face_names = []

    # Fetch only authorized images
    uploaded_images = Student_Registration.objects.filter(is_active=True)

    # Loop through each uploaded image and encode
    for student in uploaded_images:
        image_path = os.path.join(settings.MEDIA_ROOT, str(
            student.profile_image.name))  # Get the full path

        # Read the image using OpenCV
        known_image = cv2.imread(image_path)
        known_image_rgb = cv2.cvtColor(known_image, cv2.COLOR_BGR2RGB)
        encodings = detect_and_encode(known_image_rgb)

        # Append encodings and names if encoding is successful
        if encodings:
            known_face_encodings.extend(encodings)
            known_face_names.append(student.name)

    # Return the known face encodings and names
    return known_face_encodings, known_face_names


# Function to recognize faces
# Adjust threshold as needed
def recognize_faces(known_encodings, known_names, test_encodings, threshold=0.6):
    recognized_names = []  # List to store recognized names

    # Loop through each test encoding and compare with known encodings
    for test_encoding in test_encodings:
        # Calculate Euclidean distances
        distances = np.linalg.norm(known_encodings - test_encoding, axis=1)
        min_distance_idx = np.argmin(distances)

        # Check if the minimum distance is below the threshold
        if distances[min_distance_idx] < threshold:
            recognized_names.append(known_names[min_distance_idx])
        else:
            recognized_names.append('Not Recognized')
    return recognized_names


# ==================================== Helper function to check if user is admin =========================================
def is_admin(user):
    return user.is_superuser


# ======================================= View for rendering the home page ==========================================
def home(request):
    return render(request, 'index.html')


# ==================================== View for rendering the student registration page =============================
@login_required
@user_passes_test(is_admin)
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

        # Check if image_data is provided
        if image_data:
            try:
                # Split the header and the base64 data
                header, encoded = image_data.split(',', 1)
                profile_image = ContentFile(base64.b64decode(
                    # Decode and create ContentFile
                    encoded), name=f"{stu_id}.jpg")
            except Exception as e:
                messages.error(
                    request, "Error processing profile image. please try again!")
                print(f"Error decoding image: {e}")
                return render(request, 'register_stu.html')

        # Create a new Student_Registration instance
        student_registration = Student_Registration(
            stu_id=stu_id,
            name=name,
            email=email,
            phone_number=phone_number,
            designation=designation,
            department=department,
            profile_image=profile_image,
            is_active=True
        )

        # Save the student registration data to the database
        try:
            student_registration.save()
            messages.success(request, "Student Registered Successfully")
            return redirect('register_success')
        except Exception as e:
            messages.error(
                request, "Error saving student registration. Please try again.")
            print(f"Error saving student registration: {e}")
            return render(request, 'register_stu.html')

    return render(request, 'register_stu.html')


# ================================= View for rendering the registration success page ==============================
def register_success(request):
    return render(request, 'register_success.html')


# ================================= View for rendering the login page ========================================
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        # If authentication is successful, log the user in
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')


# ================================ View for logging out the user ================================
@login_required
def user_logout(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout


# =============================== View for rendering the student list page ===============================
@login_required
@user_passes_test(is_admin)
def stu_list(request):
    students = Student_Registration.objects.all()
    return render(request, 'stu_list.html', {'students': students})


# ================================= View for authorizing a student =======================================
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


# ============================== view for capturing and recognizing faces from multiple cameras ===========================
def capture_and_recognize(request):
    stop_events = []  # List to store stop events for each thread
    camera_threads = []  # List to store threads for each camera
    camera_windows = []  # List to store window names
    error_messages = []  # List to capture errors from threads

    # Thread function to process frames from a camera
    def process_frame(cam_config, stop_event):
        """Thread function to capture and process frames for each camera."""
        cap = None  # Initialize cap to None
        window_created = False  # Flag to track if the window was created
        try:
            # Check if the camera source is a number (local webcam) or a string (IP camera URL)
            if cam_config.camera_source.isdigit():
                # Use integer index for webcam
                cap = cv2.VideoCapture(int(cam_config.camera_source))
            else:
                # Use string for IP camera URL
                cap = cv2.VideoCapture(cam_config.camera_source)

            # Check if the camera opened successfully
            if not cap.isOpened():
                raise Exception(f"Unable to access camera {cam_config.name}.")

            # Get the threshold from camera configuration
            threshold = cam_config.threshold

            # Initialize pygame mixer for sound playback
            pygame.mixer.init()
            success_sound = pygame.mixer.Sound(
                'App1/suc.wav')  # Load sound path

            # Define unique window name for each camera
            window_name = f'Face Recognition - {cam_config.name}'
            camera_windows.append(window_name)  # Track the window name

            while not stop_event.is_set():      # Continue until stop_event is set
                ret, frame = cap.read()
                if not ret:
                    print(
                        f"Failed to capture frame for camera: {cam_config.name}")
                    break  # If frame capture fails, break from the loop

                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Function to detect and encode face in frame
                test_face_encodings = detect_and_encode(frame_rgb)

                if test_face_encodings:
                    # Load known face encodings once
                    known_face_encodings, known_face_names = encode_uploaded_images()
                    if known_face_encodings:
                        names = recognize_faces(np.array(
                            known_face_encodings), known_face_names, test_face_encodings, threshold)

                        # Draw bounding boxes and names on the frame
                        for name, box in zip(names, mtcnn.detect(frame_rgb)[0]):
                            if box is not None:

                                # Draw rectangle and put text
                                (x1, y1, x2, y2) = map(int, box)
                                cv2.rectangle(frame, (x1, y1),
                                              (x2, y2), (0, 255, 0), 2)
                                cv2.putText(
                                    frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                                if name != 'Not Recognized':
                                    students = Student_Registration.objects.filter(
                                        name=name)
                                    if students.exists():
                                        student = students.first()

                                        # Get current time
                                        current_time = now()

                                        # Manage attendance based on check-in and check-out logic
                                        attendance, created = Attendance.objects.get_or_create(
                                            student_registration=student, date=now().date())
                                        if created:
                                            attendance.mark_check_in()
                                            success_sound.play()
                                            cv2.putText(frame, f"{name}, checked in.", (
                                                50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                                        else:
                                            if attendance.check_in_time and not attendance.check_out_time:
                                                # Check out logic: check if 1 minute has passed after check-in
                                                time_diff = current_time - attendance.check_in_time
                                                if time_diff.total_seconds() > 60:  # 1 minute after check-in
                                                    attendance.mark_check_out()
                                                    success_sound.play()
                                                    cv2.putText(frame, f"{name}, checked out.", (
                                                        50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                                                else:
                                                    cv2.putText(frame, f"{name}, already checked in.", (
                                                        50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                                            elif attendance.check_in_time and attendance.check_out_time:
                                                cv2.putText(frame, f"{name}, already checked out.", (
                                                    50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

                # Display frame in separate window for each camera
                if not window_created:
                    cv2.namedWindow(window_name)  # Only create window once
                    window_created = True  # Mark window as created

                cv2.imshow(window_name, frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    stop_event.set()  # Signal the thread to stop when 'q' is pressed
                    break

        except Exception as e:
            print(f"Error in thread for {cam_config.name}: {e}")
            error_messages.append(str(e))  # Capture error message
        finally:
            if cap is not None:
                cap.release()
            if window_created:
                # Only destroy if window was created
                cv2.destroyWindow(window_name)

    try:
        # Get all camera configurations
        cam_configs = CameraConfiguration.objects.all()
        if not cam_configs.exists():
            raise Exception(
                "No camera configurations found. Please configure them in the admin panel.")

        # Create threads for each camera configuration
        for cam_config in cam_configs:
            stop_event = threading.Event()
            stop_events.append(stop_event)

            camera_thread = threading.Thread(
                target=process_frame, args=(cam_config, stop_event))
            camera_threads.append(camera_thread)
            camera_thread.start()

        # Keep the main thread running while cameras are being processed
        while any(thread.is_alive() for thread in camera_threads):
            time.sleep(1)  # Non-blocking wait, allowing for UI responsiveness

    except Exception as e:
        error_messages.append(str(e))  # Capture the error message
    finally:
        # Ensure all threads are signaled to stop
        for stop_event in stop_events:
            stop_event.set()

        # Ensure all windows are closed in the main thread
        for window in camera_windows:
            # Check if window exists
            if cv2.getWindowProperty(window, cv2.WND_PROP_VISIBLE) >= 1:
                cv2.destroyWindow(window)

    # Check if there are any error messages
    if error_messages:
        # Join all error messages into a single string
        full_error_message = "\n".join(error_messages)
        # Render the error page with message
        return render(request, 'error.html', {'error_message': full_error_message})

    return redirect('attendance_list')


# ==================================== View for deleting a student =====================================
@login_required
@user_passes_test(is_admin)
def stu_delete(request, pk):
    stu = get_object_or_404(Student_Registration, pk=pk)

    if request.method == 'POST':
        stu.delete()
        messages.success(request, 'Student deleted successfully.')
        # Redirect to the student list after deletion
        return redirect('stu_list')

    return render(request, 'stu_delete.html', {'stu': stu})


# ============================= View for rendering the student detail page ====================================
@login_required
@user_passes_test(is_admin)
def stu_detail(request, pk):
    stu = get_object_or_404(Student_Registration, pk=pk)
    return render(request, 'stu_detail.html', {'stu': stu})


# =============================== View for rendering the attendance list page ================================
@login_required
@user_passes_test(is_admin)
def attendance_list(request):
    # Handle search and date filter from GET params
    search_query = request.GET.get('search', '').strip()
    date_filter = request.GET.get('attendance_date', '').strip()
    download_report = request.GET.get('download_report', '')

    students = Student_Registration.objects.all()
    if search_query:
        # you can extend to stu_id or email
        students = students.filter(name__icontains=search_query)

    students_attendance_data = []
    for stu in students:
        if date_filter:
            attendance_qs = stu.attendances.filter(date=date_filter)
        else:
            attendance_qs = stu.attendances.all()

        # Only include students with at least one attendance record
        if attendance_qs.exists():
            students_attendance_data.append(
                {'students': stu, 'attendance_records': attendance_qs})

    # If user requested a CSV download, generate and return it
    if download_report.lower() == 'true':
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="attendance_report.csv"'
        writer = csv.writer(response)
        writer.writerow(['Stu Name', 'Stu ID', 'Date',
                        'Check-in Time', 'Check-out Time', 'Stayed Time'])

        for item in students_attendance_data:
            stu = item['students']
            for attendance in item['attendance_records']:
                stayed = attendance.calculate_duration() if (
                    attendance.check_in_time and attendance.check_out_time) else ''
                writer.writerow([stu.name, stu.stu_id, attendance.date,
                                attendance.check_in_time, attendance.check_out_time, stayed])

        return response

    context = {
        'students_attendance_data': students_attendance_data,
        'search_query': search_query,
        'date_filter': date_filter,
    }

    return render(request, 'attendance_list.html', context)


# ============================== view for rendering the camera_config_list template page ===========================
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
            messages.error(
                request, "A configuration with this name already exists.")
            # Render the form again to allow user to correct the error
            return render(request, 'camera_config_form.html')

    # Render the camera configuration form for GET requests
    return render(request, 'camera_config_form.html')


# ==================================== View for rendering the camera_config_list template page ====================================
@login_required
@user_passes_test(is_admin)
def camera_config_list(request):
    # Retrieve all CameraConfiguration objects from the database
    configs = CameraConfiguration.objects.all()
    # Render the list template with the retrieved configurations
    return render(request, 'camera_config_list.html', {'configs': configs})


# ================================ View for updating an existing camera configuration ===================================
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

# ============================= View for deleting an existing camera configuration ===================================
@login_required
@user_passes_test(is_admin)
def camera_config_delete(request, pk):
    # Retrieve the specific configuration by primary key or return a 404 error if not found
    config = get_object_or_404(CameraConfiguration, pk=pk)

    # Check if the request method is POST, indicating confirmation of deletion
    if request.method == "POST":
        # Delete the record from the database
        config.delete()
        # Redirect to the list of camera configurations after deletion
        return redirect('camera_config_list')

    # Render the delete confirmation template with the configuration data
    return render(request, 'camera_config_delete.html', {'config': config})
