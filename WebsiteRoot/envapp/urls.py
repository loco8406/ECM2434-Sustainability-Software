from django.urls import path
from . import views
from django.contrib.auth import views as authViews # Used for Log out function at the moment

urlpatterns = [
    path("", views.index, name="index"),
    path('register/', views.register, name='register'),  # Registration page
    path('login/', views.login_view, name='login'),
    path('gamekeeper/', views.gamekeeper, name='gamekeeper'),
    path ('Admin/', views.admin_login, name = 'Admin'), # Admin login
    path('userPortal/', views.userPortal, name='userPortal'),
    path('logout/', authViews.LogoutView.as_view(), name='logout') # Log out
]
