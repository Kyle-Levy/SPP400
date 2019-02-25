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

    def test_valid_patient(self):
        request = self.factory.post('create/', {'first_name': 'John', 'last_name': 'Smith', 'birth_date': '01/01/1950'})
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        response = new_patient(request)

        self.assertTrue(response.status_code, 200)

    def test_missing_first_name(self):
        request = self.factory.post('create/', {'last_name': 'Smith', 'birth_date': '01/01/1950'})
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        response = new_patient(request)

        self.assertTrue(response.status_code, 401)

    def test_missing_last_name(self):
        request = self.factory.post('create/', {'first_name': 'John', 'birth_date': '01/01/1950'})
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        response = new_patient(request)

        self.assertTrue(response.status_code, 401)

    def test_missing_bday(self):
        request = self.factory.post('create/', {'first_name': 'John', 'last_name': 'Smith'})
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        response = new_patient(request)

        self.assertTrue(response.status_code, 401)

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
