from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Notification
# from .forms import NotificationForm
# from .utils import send_password_reset_email
# from .decorators import add_user_context, superuser_or_teacher_required


# Create your tests here.
class NotificationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.notification = Notification.objects.create(
            user=self.user,
            title='Test Notification',
            message='This is a test notification.'
        )

    def test_notification_creation(self):
        self.assertEqual(self.notification.title, 'Test Notification')
        self.assertEqual(self.notification.message, 'This is a test notification.')
        self.assertEqual(self.notification.user.username, 'testuser')

    def test_notification_str(self):
        self.assertEqual(str(self.notification), 'Test Notification - testuser')
