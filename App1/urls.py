from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register_stu/', views.register_stu, name='register_stu'),
    path('register_success/', views.register_success, name='register_success'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('stu_list/', views.stu_list, name='stu_list'),
    path('stu-authorize/<int:pk>/', views.stu_authorize, name='stu_authorize'),
    path('stu_detail/<int:pk>/', views.stu_detail, name='stu_detail'),
    path('stu_delete/<int:pk>/delete/', views.stu_delete, name='stu_delete'),
    path('attendance_list/', views.attendance_list, name='attendance_list'),
]
