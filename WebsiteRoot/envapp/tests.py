from django.test import TestCase
from django.utils import timezone
from .models import UserTable, Videos, VideoWatchers, WaterStation, Challenge

# Tests for the user table
class UserTableTests(TestCase):
    # Set up function for testing
    def setUp(self):
        self.user = UserTable.objects.create(username='testUser', role='student')
    
    # Test getter for role
    def testGetRole(self):
        self.assertEqual(self.user.getRole(), 'student')

    # Test getter for points
    def testGetPoints(self):
        self.assertEqual(self.user.getPoints(), 0) # Ensure points default to 0 at creation

    # Test setter for Role
    def testSetRole(self):
        self.user.setRole('gamekeeper')
        self.assertEqual(self.user.getRole(), 'gamekeeper')

    # Test setter for Points
    def testSetPoints(self):
        self.user.setPoints(150)
        self.assertEqual(self.user.getPoints(), 150)

    # Test adder for points
    def testAddPoints(self):
        self.user.addPoints(50)
        self.assertEqual(self.user.getPoints(), 50)

    # Test subtracter for points
    def testSubtractPoints(self):
        self.user.setPoints(100)
        self.user.subtractPoints(20)
        self.assertEqual(self.user.getPoints(), 80)

# Tests for the Water Stations table
class WaterStationTests(TestCase):

    # Set up for testing
    def setUp(self):
        self.station = WaterStation.objects.create(
            name='Test Station',
            location_description='Description',
            longitude = 33.3213,
            latitude = 23.4543,
            points_reward=50
        )
    
    # Test adding a water station
    def testStationAddition(self):
        self.assertEqual(self.station.name, 'Test Station')
        self.assertEqual(self.station.points_reward, 50)

class ChallengeTests(TestCase):

    # Set up for testing
    def setUp(self):
        self.challenge = Challenge.objects.create(
            title='Test Challenge',
            description='Description',
            location='Test Location',
            challenge_date=timezone.now(),
            points_reward=100
        )
    
    # Test adding a challenge
    def testChallengeAddition(self):
        self.assertEqual(self.challenge.title, 'Test Challenge')
        self.assertEqual(self.challenge.points_reward, 100)
