from django import forms
from .models import Challenge


class WaterStationForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['name', 'location_description', 'location', "points_reward"]  # Fields shown in the form


