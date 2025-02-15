from django.urls import path
from django.shortcuts import redirect
from . import views


# Redirect based on user role
def home_redirect(request):
    if request.user.is_authenticated:
        if request.user.role == 'gamekeeper':
            return redirect('gamekeeper_dashboard')
        else:
            return redirect('student_dashboard')
    return redirect('login')


urlpatterns = [
    path('', home_redirect, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('gamekeeper_dashboard/', views.gamekeeper_dashboard,
         name='gamekeeper_dashboard'),
    path('edit_challenge/<int:challenge_id>/',
         views.edit_challenge, name='edit_challenge'),
    path("delete_challenge/<int:challenge_id>/",
         views.delete_challenge, name="delete_challenge"),
    path('settings/', views.settings_view, name='settings'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
]
