from django.test import TestCase, Client
from django.utils import timezone
from .models import UserTable, Videos, VideoWatchers, WaterStation, Challenge
from django.contrib.auth import get_user_model
from django.urls import reverse


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



class RegistrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.valid_user_data = {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'email': 'test@example.com',
            'role': 'user'
        }

    def test_successful_registration(self):
        response = self.client.post(self.register_url, self.valid_user_data)
        self.assertEqual(response.status_code, 302)  # Check redirect
        self.assertTrue(UserTable.objects.filter(username='testuser').exists())
        user = UserTable.objects.get(username='testuser')
        self.assertEqual(user.role, 'user')

    def test_invalid_registration_missing_fields(self):
        invalid_data = self.valid_user_data.copy()
        del invalid_data['username']
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, 200)  # Stay on same page
        self.assertFalse(UserTable.objects.filter(email='test@example.com').exists())

    def test_password_mismatch(self):
        invalid_data = self.valid_user_data.copy()
        invalid_data['password2'] = 'wrongpass'
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(UserTable.objects.filter(username='testuser').exists())

    def test_duplicate_username(self):
        # First registration
        self.client.post(self.register_url, self.valid_user_data)
        # Second registration with same username
        response = self.client.post(self.register_url, self.valid_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserTable.objects.filter(username='testuser').count(), 1)


class LoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = UserTable.objects.create_user(username='testuser', password='testpass123')

    def test_successful_login(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpass123'})
        self.assertEqual(response.status_code, 302)  # Check redirect
        self.assertTrue(response.url.endswith('/student_dashboard/'))  # Check redirect URL

    def test_invalid_login(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 200)  # Stay on same page
        self.assertContains(response, 'Invalid credentials, please try again.')


class ReferralCodeTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserTable.objects.create_user(username='testuser', password='testpass123')
        self.referrer = UserTable.objects.create_user(username='referrer', password='testpass123')
        self.referrer.referral_code = self.referrer.getCode()
        self.referrer.save()
        self.register_url = reverse('register')

    def test_valid_referral_code(self):
        valid_user_data = {
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'email': 'newuser@example.com',
            'input_referral_code': self.referrer.referral_code
        }
        response = self.client.post(self.register_url, valid_user_data)
        self.assertEqual(response.status_code, 302)  # Check redirect
        self.assertTrue(UserTable.objects.filter(username='newuser').exists())
        new_user = UserTable.objects.get(username='newuser')
        self.assertEqual(new_user.points, 25)
        self.referrer.refresh_from_db()
        self.assertEqual(self.referrer.points, 50)

    def test_invalid_referral_code(self):
        invalid_user_data = {
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'email': 'newuser@example.com',
            'input_referral_code': 'INVALIDCODE'
        }
        response = self.client.post(self.register_url, invalid_user_data)
        self.assertEqual(response.status_code, 200)  # Check that the form is re-rendered
        self.assertContains(response, "Referral code not found. No bonus points awarded.")
        self.assertFalse(UserTable.objects.filter(username='newuser').exists())
        self.referrer.refresh_from_db()
        self.assertEqual(self.referrer.points, 0)
