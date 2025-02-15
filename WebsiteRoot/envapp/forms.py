from django import forms
from .models import Challenge
from django.contrib.auth.forms import UserCreationForm
from .models import UserTable


# Challenge Form
class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['title', 'description', 'location',
                  'challenge_date', 'points_reward']
    challenge_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserTable
        fields = ("username", "password1", "password2",
                  "first_name", "last_name", "email")
