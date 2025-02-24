from django.urls import path
from . import views
from .views import generate_qr
# from map_app.views import map_view


urlpatterns = [

    #HOME PAGE URL
    path('', views.home, name='home'),
    # LOGIN SYSTEM URLS
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('delete_account/', views.delete_account, name='delete_account'),
    #STUDENT URLS
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path('settings/', views.settings_view, name='settings'),
    path('fetch_referral/', views.fetch_referral,
         name='fetch_referral'),  # New endpoint
         
    #GAMEKEEPER URLS
    path('gamekeeper_dashboard/', views.gamekeeper_dashboard,
         name='gamekeeper_dashboard'),
    path('edit_challenge/<int:challenge_id>/',
         views.edit_challenge, name='edit_challenge'),
    path("delete_challenge/<int:challenge_id>/",
         views.delete_challenge, name="delete_challenge"),
    
    #QR CODE URLS
    path('generate_qr/', generate_qr, name='generate_qr'),
    path('scanqr/', views.scanQR, name='scanQR'),
    path('scannedStation/<int:station_id>/', views.stationScanEvent, name='scannedStation'),

     #Map URLs
    
    path ('gamekeeper_map/', views.gamekeeper_map, name='gamekeeper_map'),
    path('map/', views.map_view, name='map'),  # Main page with map

]
