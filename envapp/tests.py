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
        self.user = get_user_model()
        self.register_url = reverse('register')
        self.valid_user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'role': 'user',
            'bottle_size': '500ml'
        }

    def test_registration_success(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)  # Redirect after successful registration

        response = self.client.post(self.register_url, self.valid_user_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user.objects.filter(username='testuser').exists())
        self.assertTrue(UserTable.objects.filter(username='testuser').exists())

    def test_registration_missing_fields(self):
        invalid_data = self.valid_user_data.copy()
        del invalid_data['email']
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, 200)  # Stay on same page with error
        self.assertFalse(self.user.objects.filter(username='testuser').exists())
    
    def test_registration_password_mismatch(self):
        invalid_data = self.valid_user_data.copy()
        invalid_data['password2'] = 'testpass124'
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user.objects.filter(username='testuser').exists())

    def test_registration_invalid_email(self):
        invalid_data = self.valid_user_data.copy()
        invalid_data['email'] = 'testexample.com'
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user.objects.filter(username='testuser').exists())

class LoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model()
        self.login_url = reverse('login')
        # Create a test user
        self.test_user = self.user.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.valid_login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }

    def test_login_success(self):
        """Test successful login with valid credentials"""
        response = self.client.post(self.login_url, self.valid_login_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_wrong_password(self):
        """Test login failure with wrong password"""
        invalid_data = self.valid_login_data.copy()
        invalid_data['password'] = 'testpass124'
        response = self.client.post(self.login_url, invalid_data)
        self.assertEqual(response.status_code, 200)  # Stay on login page
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_nonexistent_user(self):
        """Test login failure with non-existent username"""
        invalid_data = self.valid_login_data.copy()
        invalid_data['username'] = 'nonexistentuser'
        response = self.client.post(self.login_url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_blank_fields(self):
        """Test login failure with blank fields"""
        response = self.client.post(self.login_url, {
            'username': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


    


    


