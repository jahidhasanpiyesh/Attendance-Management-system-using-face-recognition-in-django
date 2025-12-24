# AutoAttend AI

A fully automated, AI-powered attendance management system built with **Django**, **Face Recognition**, and a secure multi-user authentication workflow. This system is designed to simplify attendance tracking for schools, offices, and organizations by using real-time face detection and recognition.

---

## 🚀 Features

### 🔹 **Advanced AI Models Used**

My project uses several high‑value AI packages from your environment. Not all packages matter for Face Recognition — but these are the important ones powering your system:

#### **Core AI & Face Recognition Packages**

* **facenet-pytorch** → Face embedding generation
* **mtcnn** → Face detection
* **torch / torchvision** → Deep learning backend
* **opencv-python** → Image capturing + preprocessing
* **numpy / scipy** → Numerical computation for recognition
* **pillow** → Image processing

#### **ML & Deep Learning Extras (Optional But Valuable)**

* **tensorflow / keras** → For training future custom face models
* **scikit‑like utilities (joblib, tqdm)** → Model optimization & progress bars
* **deepdiff** → Ideal for comparing embeddings

I’ve added this valuable package list to highlight your professional AI stack.

---

## 🖼️ Screenshots

You can add your screenshots here.
When you're ready, send them one by one — I will integrate them into this section professionally.

### 🔹 **AI-Powered Face Recognition**

* Accurate face recognition system using machine learning.
* Supports multiple users and real-time detection.
* Stores embeddings for fast and efficient recognition.

### 🔹 **User Authentication System**

* Login & logout functionality.
* Role-based access control for admin/teacher/staff.
* Secure user-level attendance dashboard.

### 🔹 **Attendance Management**

* Auto-capture and store attendance records.
* Track present/absent students with timestamps.
* View, filter, and export attendance history.

### 🔹 **Multi-User Support**

* Different permission levels for Admin, Teachers, and Students.
* Admin panel for managing users and attendance logs.

### 🔹 **Responsive UI**

* Mobile-friendly dashboard.
* Clean and modern frontend.

---

## 🛠️ Technology Stack

---

## 🔮 Future Development Roadmap (Planned Updates)

Your project is actively growing, and these enhancements will make **AutoAttend AI** a complete smart attendance ecosystem.

### ✅ **1. Multi‑Role System (Coming Soon)**

You will add 3 major user types:

* **Admin** → Full control over users, classes, subjects, reports
* **Teacher** → Take attendance, mark classes, manage students
* **Student** → View attendance history and analytics

### ✅ **2. Subject‑Wise Attendance (Planned)**

Teachers will be able to:

* Choose **subject** before starting attendance
* Select **class/section**
* Mark which class period is running
* Record **class duration automatically**

### ✅ **3. Class Duration Tracking**

System will:

* Start timer at check‑in
* Stop timer at check‑out
* Store **total class time** in database
* Generate class‑wise time reports

### ✅ **4. Check‑In / Check‑Out System**

You will create:

* **Face-based check‑in** → When entering class
* **Face-based check‑out** → When leaving
* Attendance record will show:

  * Entry time
  * Exit time
  * Total session duration

### ✅ **5. Attendance Reports & Analytics**

Planned additions:

* Monthly attendance charts
* Subject-wise analytics
* Teacher performance summaries
* CSV/Excel export option

### ✅ **6. Improved Dataset & Model Training**

Future updates will include:

* Auto image capture for dataset collection
* Retrain button from dashboard
* Live recognition confidence score display

These upcoming features make your README look **forward-thinking**, professional, and polished.

| Component       | Technology                |
| --------------- | ------------------------- |
| Backend         | Django (Python)           |
| AI/ML           | Face Recognition + OpenCV |
| Database        | SQLite / PostgreSQL       |
| Frontend        | HTML, CSS, Bootstrap      |
| Version Control | Git & GitHub              |

---

## 📦 Installation Guide

### **1️⃣ Clone the Repository**

```bash
git clone https://github.com/jahidhasanpiyesh/AutoAttend_AI.git
cd AutoAttend_AI
```

### **2️⃣ Create Virtual Environment**

```bash
python -m venv venv
venv/scripts/activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### **3️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4️⃣ Apply Migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

### **5️⃣ Run the Application**

```bash
python manage.py runserver
```

Now open your browser and go to:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🧠 Face Recognition Setup

To ensure accurate recognition:

1. Collect 20–30 images per person.
2. Store them in the assigned dataset folder.
3. Generate facial embeddings.
4. Train the recognizer before testing.

---

## 📁 Project Structure

```
AutoAttend_AI/
├── attendance/        # Attendance app logic
├── face_recognition/  # Face detection & encoding
├── users/             # Authentication & roles
├── templates/         # HTML Templates
├── static/            # CSS, JS, Images
├── manage.py
└── requirements.txt
```

---

## 🧪 Testing

Run Django tests using:

```bash
python manage.py test
```

---

## 🙌 Contribution

Pull requests are welcome!
Steps to contribute:

1. Fork the repo
2. Create a new branch
3. Commit changes
4. Submit a PR

---

---

## ⚠️ Python Version Requirement (Important)

This project only works properly with the following Python versions:

### ✅ **Supported Python Versions**

* **Python 3.12** (Recommended)
* **Python 3.11**
* **Python 3.10**

### ❌ **Not Supported**

Any version other than **3.10, 3.11, 3.12** will cause errors like:

* Package installation failure
* TensorFlow not supported
* torch/torchvision incompatibility
* Django 6.0 dependency conflicts
* Face recognition model import errors

### ⚠️ **Warning for Users (Must Read)**

If anyone wants to clone or use this project:

> **Make sure your system is running Python 3.10 / 3.11 / 3.12 only.**
> Other Python versions WILL break the project and stop AI modules from working.

---
## 🐞 Common Errors & Bugs Faced During Development

🔴 **1. Virtual Environment Accidentally Uploaded to GitHub**

* **Cause:** venv folder included
* **Fix:** Added `.gitignore`, removed venv

🔴 **2. TensorFlow Not Installing**

* **Cause:** Python version below 3.10
* **Fix:** Installed Python **3.12**

🔴 **3. torch / torchvision Version Conflict**

* **Cause:** Wrong torch build for Python version
* **Fix:**

  ```txt
  torch==2.2.2
  torchvision==0.17.2
  ```

🔴 **4. MTCNN Face Detection Error**

* **Cause:** Missing dependencies / GPU issue
* **Fix:** Reinstalled `facenet-pytorch` and `opencv-python`

🔴 **5. Django Migration Errors**

* **Cause:** Missing fields, circular references
* **Fix:**

  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

🔴 **6. Static Files Not Loading**

* **Cause:** Wrong `STATICFILES_DIRS` configuration
* **Fix:** Updated `settings.py`

🔴 **7. Login Session / Multi-User Redirect Bugs**

* **Cause:** Incorrect middleware or routing
* **Fix:** Implemented proper role-based redirection system

🔴 **8. Dataset Path Error**

* **Cause:** Wrong image path for face embeddings
* **Fix:** Used **absolute paths** instead of relative

🔴 **9. GitHub Large File (>50MB) Error**

* **Cause:** `libclang.dll` inside venv
* **Fix:** Removed venv from repo, cleaned history

🔴 **10. Webcam Lag / Frame Drop**

* **Cause:** Heavy real-time frame processing
* **Fix:** Reduced frame size + optimized model calls

## 🧩 ER Diagram (Planned)

A simplified conceptual ER diagram for the full future system:

```
Users (Admin/Teacher/Student)
    ├── id (PK)
    ├── username
    ├── password
    ├── role
    └── email

Students
    ├── id (PK)
    ├── user_id (FK → Users)
    └── class_id (FK → Class)

Teachers
    ├── id (PK)
    ├── user_id (FK → Users)
    └── subject_id (FK → Subject)

Class
    ├── id (PK)
    ├── name
    └── section

Subject
    ├── id (PK)
    ├── name
    └── class_id (FK → Class)

Attendance
    ├── id (PK)
    ├── student_id (FK → Students)
    ├── subject_id (FK → Subject)
    ├── teacher_id (FK → Teachers)
    ├── check_in_time
    ├── check_out_time
    └── duration

FaceEmbeddings
    ├── id (PK)
    ├── student_id (FK → Students)
    └── embedding_data
```

---

## 🗄️ Database Table Structure (Planned Detailed Schema)

### **users**

| Field    | Type                          | Description        |
| -------- | ----------------------------- | ------------------ |
| id       | INT PK                        | Primary key        |
| username | VARCHAR                       | Login username     |
| password | HASH                          | Encrypted password |
| role     | ENUM(admin, teacher, student) | Access level       |
| email    | VARCHAR                       | Optional           |

### **students**

| Field    | Type       |
| -------- | ---------- |
| id       | INT PK     |
| user_id  | FK → users |
| class_id | FK → class |

### **teachers**

| Field      | Type   |
| ---------- | ------ |
| id         | INT PK |
| user_id    | FK     |
| subject_id | FK     |

### **attendance**

| Field          | Type          |
| -------------- | ------------- |
| id             | INT PK        |
| student_id     | FK            |
| teacher_id     | FK            |
| subject_id     | FK            |
| check_in_time  | DATETIME      |
| check_out_time | DATETIME      |
| duration       | INT (minutes) |

---

## 📡 API Endpoints (Future Plan)

### Authentication

* `POST /api/login/`
* `POST /api/logout/`

### Students

* `GET /api/students/`
* `POST /api/students/register/`

### Teachers

* `GET /api/teachers/`
* `POST /api/teachers/register/`

### Attendance

* `POST /api/attendance/checkin/`
* `POST /api/attendance/checkout/`
* `GET /api/attendance/report/`

---

## 🧭 Use-Case Diagram (Concept)

```
Admin → Manage Users, Manage Classes, View All Reports
Teacher → Start Attendance, Check-In/Out Students, View Class Report
Student → View Attendance, View Daily/Monthly Report
```

---

## 🔁 Flowchart of Attendance Process

```
Start
 ↓
Detect Face → Match Embedding?
 ↓ Yes / No
Registered? → No → Reject
 ↓ Yes
Check-in or Check-out?
 ↓
Record Time → Update Attendance → Save Duration → End
```

---

## ⭐ Professional “About This Project” Summary

AutoAttend AI is an intelligent face-recognition–powered attendance management system designed for educational institutes, offices, and organizations.
Using deep learning models like **MTCNN** and **FaceNet**, the system performs accurate real-time face identification and automates all attendance operations.
Future upgrades include multi-role dashboards, subject-wise attendance, analytics, and a smart check-in/check-out system.

---

## 🏷️ GitHub Badges (Add to README Header)

```
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-6.0-success)
![License](https://img.shields.io/badge/license-MIT-blue)
```

---

## 🎨 Project Logo (Placeholder)

You can upload your preferred logo OR I can design a simple one such as:

* AI + Attendance icon
* Face-recognition styled logo
* Minimalistic flat design

Upload an image OR tell me your style, and I will generate the logo.

---
## 🛡️ License

This project is licensed under the **GNU General Public License v3.0**. 

### ⚖️ Permissions under GPLv3:
* **Commercial Use:** You can use this software for commercial purposes.
* **Modification:** You can modify the code, but you must keep the source code open.
* **Distribution:** You can distribute the original or modified code.
* **Credit:** You must give credit to the original author (Md Jahid Hasan).

See the [LICENSE](LICENSE) file for more details.

---
## 👤 Author

- Developer: Md Jahid Hasan  
- Email: jahidhasanpiyesh@gmail.com  
- LinkedIn: [https://www.linkedin.com/in/md-jahid-hasan-9418b9298](https://www.linkedin.com/in/md-jahid-hasan-9418b9298)  
- Portfolio: [https://jahidhasanpiyesh.github.io/](https://jahidhasanpiyesh.github.io/)  
