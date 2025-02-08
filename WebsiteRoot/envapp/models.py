from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserTable(AbstractUser):
    # This extends the included User model
    role = models.CharField(max_length=30)
    points = models.IntegerField(default=0)

class Videos(models.Model):
    #This stores the videos for the eventual video watching task
    videoTitle = models.CharField(max_length=200) # For video title
    videoThumbnailURL = models.CharField(max_length=200) # For link to an image file to display as a thumbnail
    videoLink = models.CharField(max_length=200) # Actual link to the video
    videoPoints = models.IntegerField(default=0, null=False) # Number of points given for watching

    def __str__(self):
        return self.videoTitle

class VideoWatchers(models.Model):
    userID = models.ForeignKey(UserTable, on_delete=models.CASCADE) # Stores the user ID of the user who has watched the video
    videoID = models.ForeignKey(Videos, on_delete=models.CASCADE) # Stores the video ID of the video that has been watched
    watchTime = models.DateTimeField(auto_now_add=True) # Automatically adds the date the video has been watched/clicked

class Challenge(models.Model):
    title = models.CharField(max_length=200)  # Challenge title
    description = models.TextField()  # Challenge details
    location = models.TextField()
    challenge_date = models.DateTimeField()
    points_reward = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when created

    def __str__(self):
        return self.title
