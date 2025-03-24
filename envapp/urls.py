from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.conf.urls import handler404
from .views import gamekeeper_map, map_view, report_water_station, reset_report, custom_404

urlpatterns = [
    # HOME PAGE URL
    path('', views.home, name='home'),

    # LOGIN SYSTEM URLS
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('delete_account/', views.delete_account, name='delete_account'),

    # STUDENT URLS
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path('settings/', views.settings_view, name='settings'),
    path('fetch_referral/', views.fetch_referral,
         name='fetch_referral'),
    path("update-profile-picture/", views.update_profile_picture,
         name="update_profile_picture"),
    path("remove-profile-picture/", views.remove_profile_picture,
         name="remove_profile_picture"),

    # GAMEKEEPER URLS
    path('gamekeeper_dashboard/', views.gamekeeper_dashboard,
         name='gamekeeper_dashboard'),
    path('createChallenge/',
         views.createChallenge, name='createChallenge'),
    path('challengeList/',
         views.challengeList, name='challengeList'),
    path('edit_challenge/<int:challenge_id>/',
         views.edit_challenge, name='edit_challenge'),
    path("delete_challenge/<int:challenge_id>/",
         views.delete_challenge, name="delete_challenge"),
    path('challenges/<int:challenge_id>/', views.assignStationToChallenge, name='challengeDetail'),
    path('challenge/<int:challenge_id>/assign/', views.assignStationToChallenge, name='assignStationToChallenge'),

    # QR CODE URLS
    path('generate_qr/', views.generate_qr, name='generate_qr'),
    path('scanqr/', views.scanQR, name='scanQR'),
    path('scannedStation/<int:station_id>/',
         views.stationScanEvent, name='scannedStation'),

    # Map URLs
    path('gamekeeper_map/', views.gamekeeper_map, name='gamekeeper_map'),
    path('map/', views.map_view, name='map'),  # Main page with map
    path('report_water_station/<int:station_id>/', report_water_station, name='report_water_station'),
    path('reset_report/<int:station_id>/', reset_report, name='reset_report'),
    
    # GAME URLs
    path('sippyBottle/', views.sippyBottle, name='sippyBottle'),
    path('api/fuel/', views.getFuel, name='getFuel'),
    path('pointUpdate/<int:newPointValue>/',
         views.updateFuelEvent, name='updateFuelEvent'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
handler404 = "envapp.views.custom_404"