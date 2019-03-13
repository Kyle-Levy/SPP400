from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware

from .views import error

class TestLogin(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware()
        self.user = User.objects.create_superuser('testuser', 'testuser@email.com', 'supersecretpass')
        self.user.save()

    def test_error_page(self):
        request = self.factory.post('')
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = error(request)
        self.assertEqual(response.status_code, 200)
