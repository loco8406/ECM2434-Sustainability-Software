from django.urls import path
from . import views
from .views import generate_qr
# from map_app.views import map_view


urlpatterns = [
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
    path('fetch_referral/', views.fetch_referral,
         name='fetch_referral'),  # New endpoint
    path('generate_qr/', generate_qr, name='generate_qr'),
    # path('read_only-map/', readonly_map, name='read_only_map'),
    # path('gamekeeper-map/', gamekeeper_map, name='gamekeeper_map'),
    # path('get-locations/', get_locations, name='get_locations'),
]
