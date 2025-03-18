from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import random
import string


# Create your models here.
def generate_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Creation of the challenge model


class Challenge(models.Model):
    title = models.CharField(max_length=200)  # Challenge title
    description = models.TextField()  # Challenge details
    location = models.TextField()
    challenge_date = models.DateTimeField()
    points_reward = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UserTable(AbstractUser):
    role = models.CharField(max_length=30, default='user')
    points = models.IntegerField(default=0)
    referral_code = models.CharField(
        max_length=10, blank=True, null=True, unique=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', blank=True, null=True)
    consent_timestamp = models.DateTimeField(auto_now_add=True)
    fuelRemaining = models.IntegerField(default=0)

    def getRole(self):
        return self.role

    def getPoints(self):
        return self.points

    def setRole(self, newRole):
        self.role = newRole
        self.save()

    def setPoints(self, newPoints):
        self.points = newPoints
        self.save()

    def addPoints(self, pointsScored):
        self.points += pointsScored
        self.save()

    def subtractPoints(self, pointsLost):
        self.points -= pointsLost
        self.save()
        
    def getCode(self):
        """Generate and save a referral code if one does not already exist."""
        if not self.referral_code:
            self.referral_code = generate_code()
            self.save()
        return self.referral_code


class Videos(models.Model):
    # This stores the videos for the eventual video watching task
    videoTitle = models.CharField(max_length=200)  # For video title
    # For link to an image file to display as a thumbnail
    videoThumbnailURL = models.CharField(max_length=200)
    videoLink = models.CharField(max_length=200)  # Actual link to the video
    # Number of points given for watching
    videoPoints = models.IntegerField(default=0, null=False)

    def __str__(self):
        return self.videoTitle


class VideoWatchers(models.Model):
    # Stores the user ID of the user who has watched the video
    userID = models.IntegerField()
    # Stores the video ID of the video that has been watched
    videoID = models.IntegerField()
    # Automatically adds the date the video has been watched/clicked
    watchTime = models.DateTimeField(auto_now_add=True)


class WaterStation(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location_description = models.TextField()
    points_reward = models.IntegerField(default=0)


class StationUsers(models.Model):
    # Stores the user ID of the user who has used the Water Station
    userID = models.IntegerField()
    # Stores the ID of the water station that has been used
    waterStationID = models.IntegerField()
    # Automatically adds the date the station has been used
    fillTime = models.DateTimeField(auto_now_add=True)

    def get_formatted_date(self):
        return self.fillTime.strftime("%B %d, %Y at %I:%M %p")

    class Meta:
        ordering = ['-fillTime']
