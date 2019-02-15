from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware

from .views import log_in


# Create your tests here.
class TestLogin(TestCase):

    # create setUp so every test can have access to the requestFactory
    # Needed to add session to the request: https://medium.com/@harshvb7/how-to-add-session-and-messages-in-django-requestfactory-16935a3351d0
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware()
        user = User.objects.create_superuser('testuser', 'testuser@email.com', 'super_secret_pass')
        user.save()

    def test_login_page_good_credentials(self):
        request = self.factory.post('login/', {'username': 'testuser', 'password': 'super_secret_pass'})

        self.middleware.process_request(request)
        request.session.save()

        response = log_in(request)

        self.assertEqual(response.status_code, 200)

    def test_login_page_wrong_password(self):
        request = self.factory.post('login/', {'username': 'testuser', 'password': 'soup_secret_pass'})

        self.middleware.process_request(request)
        request.session.save()

        response = log_in(request)

        self.assertEqual(response.status_code, 401)

    def test_login_page_wrong_username(self):
        request = self.factory.post('login/', {'username': '418', 'password': 'super_secret_pass'})

        self.middleware.process_request(request)
        request.session.save()

        response = log_in(request)

        self.assertEqual(response.status_code, 401)

    def test_login_page_missing_username(self):
        request = self.factory.post('login/', {'password': 'super_secret_pass'})

        self.middleware.process_request(request)
        request.session.save()

        response = log_in(request)

        self.assertIsNone(response)

    def test_login_page_missing_password(self):
        request = self.factory.post('login/', {'username': 'testuser'})

        self.middleware.process_request(request)
        request.session.save()

        response = log_in(request)

        self.assertIsNone(response)
