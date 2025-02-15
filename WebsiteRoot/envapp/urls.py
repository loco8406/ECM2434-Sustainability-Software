from django.urls import path
from django.shortcuts import redirect
from . import views

# Function to redirect '/' to the correct dashboard


def home_redirect(request):
    if request.user.is_authenticated:
        if request.user.role == 'gamekeeper':
            return redirect('gamekeeper_dashboard')
        else:
            return redirect('student_dashboard')
    return redirect('login')  # If not logged in, send to login


urlpatterns = [
    path('', home_redirect, name='home'),  # Redirect '/' to the right page
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('gamekeeper_dashboard/', views.gamekeeper_dashboard,
         name='gamekeeper_dashboard'),
    path('settings/', views.settings_view, name='settings'),
    path('delete_account/', views.delete_account, name='delete_account'),
]
