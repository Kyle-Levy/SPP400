from django.test import RequestFactory, TestCase
from django.contrib.sessions.middleware import SessionMiddleware
from .views import index

class TestProcedures(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_procedures_post(self):
        request = self.factory.post('index/', {'procedure_name': 'blood test'})
        request.user = None
        self.middleware.process_request(request)
        request.session.save()

        response = index(request)
        self.assertEqual(response.status_code, 200)

    def test_procedures_other(self):
        request = self.factory.get('index/', {'procedure_name': 'blood test'})
        request.user = None
        self.middleware.process_request(request)
        request.session.save()

        response = index(request)
        self.assertEqual(response.status_code, 200)
