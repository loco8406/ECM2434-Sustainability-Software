from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import random

# Create your models here.

class UserTable(AbstractUser):
    # This extends the included User model 
    role = models.CharField(max_length=30, default='user')  
    points = models.IntegerField(default=0) # Keeps track of this user's points
    
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

class Videos(models.Model):
    #This stores the videos for the eventual video watching task
    videoTitle = models.CharField(max_length=200) # For video title
    videoThumbnailURL = models.CharField(max_length=200) # For link to an image file to display as a thumbnail
    videoLink = models.CharField(max_length=200) # Actual link to the video
    videoPoints = models.IntegerField(default=0, null=False) # Number of points given for watching

    def __str__(self):
        return self.videoTitle

class VideoWatchers(models.Model):
    userID = models.IntegerField() # Stores the user ID of the user who has watched the video
    videoID = models.IntegerField() # Stores the video ID of the video that has been watched
    watchTime = models.DateTimeField(auto_now_add=True) # Automatically adds the date the video has been watched/clicked

class WaterStation(models.Model):
    name = models.CharField(max_length=200)
    location_description = models.TextField()
    location = models.TextField()
    points_reward = models.IntegerField(default=0)

class Challenge(models.Model):
    title = models.CharField(max_length=200)  # Challenge title
    description = models.TextField()  # Challenge details
    location = models.TextField()
    challenge_date = models.DateTimeField()
    points_reward = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when created

    def __str__(self):
        return self.title
