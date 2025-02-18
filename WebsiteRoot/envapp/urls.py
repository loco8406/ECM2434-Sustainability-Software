from django.urls import path

from . import views
from .views import generate_qr
from map_app.views import map_view


urlpatterns = [
    path("", views.index, name="index"),
    path('register/', views.register, name='register'),  # Registration page
    path('login/', views.login_view, name='login'),
    path('gamekeeper/', views.gamekeeper, name='gamekeeper'),
    path('Admin/', views.admin_login, name = 'Admin'), # Admin login
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),  # Add this line
    path('fetch_referral/', views.fetch_referral, name='fetch_referral'),  # New endpoint
    path('generate_qr/', generate_qr, name='generate_qr'),
    path('admin/', admin.site.urls),
    path('read_only-map/', readonly_map, name='read_only_map'),
    path('gamekeeper-map/', gamekeeper_map, name='gamekeeper_map'),
    path('get-locations/', get_locations, name='get_locations'),
]
