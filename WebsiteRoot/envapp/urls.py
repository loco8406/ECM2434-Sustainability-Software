from django.urls import path
from .views import challenge_list, create_challenge, edit_challenge, delete_challenge
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('register/', views.register, name='register'),  # Registration page
    path('login/', views.login_view, name='login'),
    path('gamekeeper/', views.gamekeeper, name='gamekeeper'),
    path('Admin/', views.admin_login, name = 'Admin'), # Admin login
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),  # Add this line
    path('review-submissions/', review_submissions, name='review_submissions'), #review_submissions
    path('challenges/', challenge_list, name='challenge_list'),
    path('challenges/create/', create_challenge, name='create_challenge'),
    path('challenges/edit/<int:challenge_id>/', edit_challenge, name='edit_challenge'),
    path('challenges/delete/<int:challenge_id>/', delete_challenge, name='delete_challenge'),
]
