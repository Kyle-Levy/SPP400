from django.test import RequestFactory, TestCase
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User
from .views import index, new_procedure
from .models import Procedures


class TestProcedures(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware()
        self.user = User.objects.create_superuser('testuser', 'testuser@email.com', 'supersecretpass')
        self.user.save()

    def test_procedures_post(self):
        request = self.factory.post('create/', {'procedure_name': 'blood test', 'notes' : 'A blood test is a laboratory analysis performed on a blood sample that is usually extracted from a vein in the arm using a hypodermic needle, or via fingerprick.'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = new_procedure(request)
        self.assertEqual(response.status_code, 200)

        created_procedure = Procedures.objects.get(procedure_name= 'blood test', notes='A blood test is a laboratory analysis performed on a blood sample that is usually extracted from a vein in the arm using a hypodermic needle, or via fingerprick.')
        self.assertIsNotNone(created_procedure)

    def test_procedures_other(self):
        request = self.factory.get('index/', {'procedure_name': 'blood test'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = index(request)
        self.assertEqual(response.status_code, 200)
