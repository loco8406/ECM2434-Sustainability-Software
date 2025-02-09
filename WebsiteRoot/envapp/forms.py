from django import forms
from .models import Challenge
from django.contrib.auth.forms import UserCreationForm
from .models import UserTable, Videos


class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['title', 'description', 'location', 'challenge_date', "points_reward"]  # Fields shown in the form

    challenge_date = forms.DateTimeField(

        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserTable
        fields = ("username", "password1", "password2", "first_name", "last_name", "email")
        
class VideoForm(forms.ModelForm):
    class Meta:
        model = Videos
        fields = ['videoTitle', 'videoThumbnailURL', 'videoLink', 'videoPoints']
        # This basically changes the labels of the form on the user's end
        labels = {
            'videoTitle': 'Title of the Video',
            'videoThumbnailURL': 'Thumbnail Image URL',
            'videoLink': 'Video URL',
            'videoPoints': 'Points for Watching'
        }
