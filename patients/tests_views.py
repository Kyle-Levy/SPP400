from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware

from .views import index, new_patient


# Create your tests here.
class TestLogin(TestCase):
    # create setUp so every test can have access to the requestFactory
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware()
        self.user = User.objects.create_superuser('testuser', 'testuser@email.com', 'super_secret_pass')
        self.user.save()

    def test_get_patients(self):
        request = self.factory.get('/patients/')

        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        response = index(request)

        self.assertTrue(response.status_code, 200)

    def test_get_new_patients(self):
        request = self.factory.get('/patients/create/')

        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        response = new_patient(request)

        self.assertTrue(response.status_code, 200)
