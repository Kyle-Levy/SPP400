from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware

from .views import *
from .models import Patients
from django.contrib.messages.storage.fallback import FallbackStorage


# Create your tests here.
class TestAnalytics(TestCase):
    # create setUp so every test can have access to the requestFactory
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware()
        self.user = User.objects.create_superuser('testuser', 'testuser@email.com', 'super_secret_pass')
        self.user.save()

    def test_get_index(self):

        request = self.factory.get('/analytics/')
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        response = index(request)

        self.assertEqual(response.status_code, 200)
