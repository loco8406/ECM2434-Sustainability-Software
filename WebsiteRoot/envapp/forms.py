from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserTable, WaterStation, Challenge

# Form for challenges created by the Gamekeeper


class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['title', 'description', 'location', 'challenge_date',
                  "points_reward"]  # Fields shown in the form

# Form for Water station created by the Gamekeeper


class WaterStationForm(forms.ModelForm):
    class Meta:
        model = WaterStation
        fields = ['name', 'latitude', 'longitude',
                  'location_description', 'points_reward','photo']
        photo = forms.ImageField(required=False)
        widgets = {
            "location_description": forms.Textarea(attrs={"rows": 3}),
        }


class CustomUserCreationForm(UserCreationForm):
    BOTTLE_SIZE_CHOICES = [
        ("500ml", "500ml"),
        ("750ml", "750ml"),
        ("1000ml", "1L"),
        ("1500ml", "1.5L"),
        ("2000ml", "2L"),
    ]

    bottle_size = forms.ChoiceField(
        choices=BOTTLE_SIZE_CHOICES,
        required=True,
        label="Estimated Bottle Size",
        help_text="Select the size of your reusable bottle."
    )
    
    input_referral_code = forms.CharField(
        required=False,
        max_length=10,
        label="Referral Code",
        help_text="Enter a referral code if you have one."
    )
    BOTTLE_SIZE_CHOICES = [
        ("500ml", "500ml"),
        ("750ml", "750ml"),
        ("1000ml", "1L"),
        ("1500ml", "1.5L"),
        ("2000ml", "2L"),
    ]

    bottle_size = forms.ChoiceField(
        choices=BOTTLE_SIZE_CHOICES,
        required=True,
        label="Estimated Bottle Size",
        help_text="Select the size of your reusable bottle."
    )
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
=======

>>>>>>> Stashed changes

    class Meta:
        model = UserTable
        fields = ["username", "password1", "password2",
<<<<<<< Updated upstream
<<<<<<< Updated upstream
                  "first_name", "last_name", "email", "bottle_size"]
=======
                  "first_name", "last_name", "email","bottle_size"]
>>>>>>> Stashed changes
=======
                  "first_name", "last_name", "email","bottle_size"]
>>>>>>> Stashed changes
