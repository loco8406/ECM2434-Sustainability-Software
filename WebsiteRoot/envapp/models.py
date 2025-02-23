from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import random
import string


# Create your models here.
def generate_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


class Challenge(models.Model):
    title = models.CharField(max_length=200)  # Challenge title
    description = models.TextField()  # Challenge details
    location = models.TextField()
    challenge_date = models.DateTimeField()
    points_reward = models.IntegerField(default=0)
    created_at = models.DateTimeField(
        auto_now_add=True)  # Timestamp when created

    def __str__(self):
        return self.title


class UserTable(AbstractUser):
    # This extends the included User model
    role = models.CharField(max_length=30, default='user')
    # Keeps track of this user's points
    points = models.IntegerField(default=0)
    referral_code = models.CharField(
        max_length=10, blank=True, null=True, unique=True)

    # Returns the role of the user

    def getRole(self):
        return self.role

    # Returns the number of points
    def getPoints(self):
        return self.points

    # Sets the role of the user
    def setRole(self, newRole):
        self.role = newRole
        self.save()

    # Overrides the current points value a new one (SHOULD NOT BE USED EXCEPT FOR ADMIN FUNCTIONS, OTHERWISE USE addPoints/subtractPoints)
    def setPoints(self, newPoints):
        self.points = newPoints
        self.save()

    # Increases the points by a specified amount
    def addPoints(self, pointsScored):
        self.points += pointsScored
        self.save()

    # Decreases the points by a specified amount (Unsure of use case yet, perhaps for ADMIN?)
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
    location_description = models.TextField()
    location = models.TextField()
    points_reward = models.IntegerField(default=0)
