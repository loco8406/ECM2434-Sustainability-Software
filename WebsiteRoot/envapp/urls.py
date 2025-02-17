from django.urls import path
from . import views
from .views import generate_qr

urlpatterns = [
    path("", views.index, name="index"),
    path('register/', views.register, name='register'),  # Registration page
    path('login/', views.login_view, name='login'),
    path('gamekeeper/', views.gamekeeper, name='gamekeeper'),
    path('Admin/', views.admin_login, name = 'Admin'), # Admin login
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),  # Add this line
    path('generate_qr/', generate_qr, name='generate_qr'),
    path('scanqr/', views.scanQR, name='scanQR'),
]
