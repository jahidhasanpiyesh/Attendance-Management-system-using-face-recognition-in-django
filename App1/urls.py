from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register_stu/', views.register_stu, name='register_stu'),
    path('register_success/', views.register_success, name='register_success'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('stu_list/', views.stu_list, name='stu_list'),
    path('stu_authorize/<int:pk>/', views.stu_authorize, name='stu_authorize'), # use pk to identify student
    path('stu_detail/<int:pk>/', views.stu_detail, name='stu_detail'),
    path('stu_delete/<int:pk>/delete/', views.stu_delete, name='stu_delete'),
    path('attendance_list/', views.attendance_list, name='attendance_list'),
    path('capture_and_recognize/', views.capture_and_recognize,
         name='capture_and_recognize'),
    path('camera_config/', views.camera_config_create,
         name='camera_config_create'),
    path('camera_config/list/', views.camera_config_list,
         name='camera_config_list'),
    path('camera_config/update/<int:pk>/',
         views.camera_config_update, name='camera_config_update'),
    path('camera-config/delete/<int:pk>/',
         views.camera_config_delete, name='camera_config_delete'),
]
