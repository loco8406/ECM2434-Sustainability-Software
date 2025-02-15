from django.db import models
from django.contrib.auth.models import AbstractUser


# User Model
class UserTable(AbstractUser):
    role = models.CharField(max_length=30, default='user')
    points = models.IntegerField(default=0)

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
        self.points += pointsLost
        self.save()


# Challeng Model
class Challenge(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.TextField()
    challenge_date = models.DateTimeField()
    points_reward = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Videos(models.Model):
    videoTitle = models.CharField(max_length=200)  # For video title
    videoThumbnailURL = models.CharField(max_length=200)
    videoLink = models.CharField(max_length=200)  # Actual link to the video
    videoPoints = models.IntegerField(default=0, null=False)

    def __str__(self):
        return self.videoTitle


class VideoWatchers(models.Model):
    userID = models.IntegerField()
    videoID = models.IntegerField()
    watchTime = models.DateTimeField(auto_now_add=True)
