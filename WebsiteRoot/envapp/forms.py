from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserTable, WaterStation


class WaterStationForm(forms.ModelForm):
    class Meta:
        model = WaterStation
        fields = ['name', 'location_description', 'location', "points_reward"]  # Fields shown in the form





class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserTable
        fields = ("username", "password1", "password2", "first_name", "last_name", "email")
