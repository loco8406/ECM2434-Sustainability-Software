from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# Create your models here.

class UserTable(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('gamekeeper', 'Gamekeeper'),
        ('admin', 'Admin'),
    ]
    # This extends the included User model 
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
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
        self.points += pointsLost
        self.save()

class Videos(models.Model):
    #This stores the videos for the eventual video watching task
    videoTitle = models.CharField(max_length=200) # For video title
    videoThumbnailURL = models.CharField(max_length=200) # For link to an image file to display as a thumbnail
    videoLink = models.CharField(max_length=200) # Actual link to the video
    videoPoints = models.IntegerField(default=1, null=False) # Number of points given for watching

    def __str__(self):
        return self.videoTitle

class VideoWatchers(models.Model):
    userID = models.IntegerField() # Stores the user ID of the user who has watched the video
    videoID = models.IntegerField() # Stores the video ID of the video that has been watched
    watchTime = models.DateTimeField(auto_now_add=True) # Automatically adds the date the video has been watched/clicked

class Challenge(models.Model):
    title = models.CharField(max_length=200)  # Challenge title
    description = models.TextField()  # Challenge details
    challenge_date = models.DateTimeField()
    points_reward = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when created

    def __str__(self):
        return self.title

class PublicTransportChallenge(Challenge):
    image_submission = models.ImageField(upload_to='tickets/')  # Upload ticket image

class BarcodeChallenge(Challenge):
    product_name = models.CharField(max_length=200)  # Name of sustainable product
    barcode_value = models.CharField(max_length=100)  # Expected barcode value

class EventChallenge(Challenge):
    location = models.TextField()
    challenge_date = models.DateTimeField()
    attended_users = models.ManyToManyField(User, blank=True)  # Users who attended

class QuizChallenge(Challenge):
    quiz_question = models.TextField()


class ChallengeParticipation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    submission_text = models.TextField(blank=True, null=True)  # For quiz answers
    image_submission = models.ImageField(upload_to='submissions/', blank=True, null=True)  # For tickets
    barcode_scan = models.CharField(max_length=100, blank=True, null=True)  # For barcode challenges
    attended = models.BooleanField(default=False)  # For events
    reviewed = models.BooleanField(default=False)  # If admin has checked the submission
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"

def review_submission(request, submission_id):
    submission = ChallengeSubmission.objects.get(id=submission_id)
    
    if submission.reviewed is False:
        submission.reviewed = True
        submission.user.points += submission.challenge.points_reward  # Add points
        submission.user.save()
        submission.save()

    return redirect('review_page')
