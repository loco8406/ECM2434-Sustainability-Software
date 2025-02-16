from django import forms
from .models import Challenge, WaterStation
from django.contrib.auth.forms import UserCreationForm
from .models import UserTable


class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['title', 'description', 'location', 'challenge_date', "points_reward"]  # Fields shown in the form

    challenge_date = forms.DateTimeField(

        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
class WaterStationForm(forms.ModelForm):
    class Meta:
        model = WaterStation
        fields = ['name', 'location_description', 'location', "points_reward"]



class CustomUserCreationForm(UserCreationForm):
    input_referral_code = forms.CharField(
        required=False,
        max_length=10,
        label="Referral Code",
        help_text="Enter a referral code if you have one."
    )
    class Meta:
        model = UserTable
        fields = ("username", "password1", "password2", "first_name", "last_name", "email",)