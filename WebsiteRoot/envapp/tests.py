from django.test import TestCase
from django.utils import timezone
from .models import UserTable, Videos, VideoWatchers, WaterStation, Challenge

class UserTableTests(TestCase):

    def setUp(self):
        self.user = UserTable.objects.create(username='testuser', role='admin', points=100)
    
    def test_get_role(self):
        self.assertEqual(self.user.getRole(), 'admin')

    def test_get_points(self):
        self.assertEqual(self.user.getPoints(), 100)

    def test_set_role(self):
        self.user.setRole('superadmin')
        self.assertEqual(self.user.getRole(), 'superadmin')

    def test_set_points(self):
        self.user.setPoints(150)
        self.assertEqual(self.user.getPoints(), 150)

    def test_add_points(self):
        self.user.addPoints(50)
        self.assertEqual(self.user.getPoints(), 150)

    def test_subtract_points(self):
        self.user.subtractPoints(20)
        self.assertEqual(self.user.getPoints(), 80)

class VideosTests(TestCase):

    def setUp(self):
        self.video = Videos.objects.create(
            videoTitle='Test Video',
            videoThumbnailURL='http://example.com/thumb.jpg',
            videoLink='http://example.com/video.mp4',
            videoPoints=10
        )
    
    def test_video_str(self):
        self.assertEqual(str(self.video), 'Test Video')

class VideoWatchersTests(TestCase):

    def setUp(self):
        self.video_watcher = VideoWatchers.objects.create(
            userID=1,
            videoID=1
        )
    
    def test_video_watcher_creation(self):
        self.assertEqual(self.video_watcher.userID, 1)
        self.assertEqual(self.video_watcher.videoID, 1)

class WaterStationTests(TestCase):

    def setUp(self):
        self.station = WaterStation.objects.create(
            name='Test Station',
            location_description='Description',
            location='Test Location',
            points_reward=50
        )
    
    def test_station_creation(self):
        self.assertEqual(self.station.name, 'Test Station')
        self.assertEqual(self.station.points_reward, 50)

class ChallengeTests(TestCase):

    def setUp(self):
        self.challenge = Challenge.objects.create(
            title='Test Challenge',
            description='Description',
            location='Test Location',
            challenge_date=timezone.now(),
            points_reward=100
        )
    
    def test_challenge_creation(self):
        self.assertEqual(self.challenge.title, 'Test Challenge')
        self.assertEqual(self.challenge.points_reward, 100)
