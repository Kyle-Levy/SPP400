from django.contrib.auth import authenticate
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from datetime import timedelta
from django.utils import timezone

from .views import log_in, log_out, authenticator, homepage


# Create your tests here.
class TestLogin(TestCase):
    # create setUp so every test can have access to the requestFactory
    # Needed to add session to the request: https://medium.com/@harshvb7/how-to-add-session-and-messages-in-django-requestfactory-16935a3351d0
    '''
    Tests were failing with the error:
    ValueError: modules context processor requires "django.contrib.auth.context_processors.auth"
    to be in TEMPLATE_CONTEXT_PROCESSORS in your settings file.

    This person had a similar issue with their fix being done below:
    https://stackoverflow.com/questions/50513310/django-test-will-not-notice-django-contrib-auth-context-processors-auth/50514240#50514240
    '''

    # A request must have a user tied to it, but a login can still be unsuccessful if the data posted is invalid
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware()
        self.user = User.objects.create_superuser('testuser', 'testuser@email.com', 'super_secret_pass')
        self.user.save()

    def test_login_page_good_credentials_good_auth(self):
        request = self.factory.post('login/', {'username': 'testuser', 'password': 'super_secret_pass'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = log_in(request)
        self.assertEqual(response.status_code, 200)

        userObj = authenticate(username=request.session['username'], password=request.session['password'])

        authRequest = self.factory.post('authenticator/', {'key': userObj.profile.key})
        authRequest.user = self.user

        # Grab the session cookies from the previous post
        authRequest.session = request.session
        authRequest.session.save()

        authResponse = authenticator(authRequest)

        self.assertEqual(authResponse.status_code, 302)

    def test_login_page_good_credentials_good_auth_case_mismatch(self):
        request = self.factory.post('login/', {'username': 'testUSER', 'password': 'super_secret_pass'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = log_in(request)
        self.assertEqual(response.status_code, 200)

        userObj = authenticate(username=request.session['username'], password=request.session['password'])

        authRequest = self.factory.post('authenticator/', {'key': userObj.profile.key})
        authRequest.user = self.user

        # Grab the session cookies from the previous post
        authRequest.session = request.session
        authRequest.session.save()

        authResponse = authenticator(authRequest)

        self.assertEqual(authResponse.status_code, 302)

    def test_login_page_good_credentials_bad_auth(self):
        request = self.factory.post('login/', {'username': 'testuser', 'password': 'super_secret_pass'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = log_in(request)
        self.assertEqual(response.status_code, 200)

        userObj = authenticate(username=request.session['username'], password=request.session['password'])

        authRequest = self.factory.post('authenticator/', {'key': 1})
        authRequest.user = self.user

        # Grab the session cookies from the previous post
        authRequest.session = request.session
        authRequest.session.save()

        authResponse = authenticator(authRequest)

        self.assertEqual(authResponse.status_code, 401)

    def test_login_page_good_credentials_no_auth_needed(self):
        request = self.factory.post('login/', {'username': 'testuser', 'password': 'super_secret_pass'})
        request.user = self.user

        # Fast forward the key expiration so its valid
        request.user.profile.key_expiration = timezone.now() + timedelta(days=30)
        self.middleware.process_request(request)
        request.session.save()
        request.user.save()

        response = log_in(request)

        self.assertEqual(response.status_code, 302)

    def test_login_page_wrong_password(self):
        request = self.factory.post('login/', {'username': 'testuser', 'password': 'soup_secret_pass'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = log_in(request)

        self.assertEqual(response.status_code, 401)

    def test_login_page_wrong_username(self):
        request = self.factory.post('login/', {'username': '418', 'password': 'super_secret_pass'})
        request.user = self.user
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

    def test_get_login_page(self):
        request = self.factory.get('/login/')

        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        response = log_in(request)

        self.assertEqual(response.status_code, 200)

    def test_get_homepage(self):
        request = self.factory.get('/homepage/')

        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        response = homepage(request)

        self.assertEqual(response.status_code, 200)


class TestLogout(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware()
        self.user = User.objects.create_superuser('testuser', 'testuser@email.com', 'super_secret_pass')
        self.user.save()

    def test_logout(self):
        request = self.factory.post('login/', {'username': 'testuser', 'password': 'super_secret_pass'})
        request.user = self.user

        self.middleware.process_request(request)
        request.session.save()

        log_in(request)
        self.assertTrue(request.user.is_authenticated)

        log_out(request)

        self.assertFalse(request.user.is_authenticated)
