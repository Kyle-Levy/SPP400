from django.test import RequestFactory, TestCase
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User
from .views import index, new_procedure, view_procedure, update_procedure, delete_procedure
from .models import Procedure


class TestProcedures(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware()
        self.user = User.objects.create_superuser('testuser', 'testuser@email.com', 'supersecretpass')
        self.user.save()

        #Creating procedure for testing the ability to manipulate a procedure
        request = self.factory.post('create/', {'procedure_name': 'View Procedure','notes': 'These are test notes'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()
        new_procedure(request)
        self.test_procedure = Procedure.objects.get(procedure_name='View Procedure',
                                                    procedure_info='These are test notes')

    def test_create_new_procedure(self):
        request = self.factory.post('create/', {'procedure_name': 'Leeches',
                                                'notes': 'have been used for clinical bloodletting for at least 2,500 years'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = new_procedure(request)
        self.assertEqual(response.status_code, 302)

        created_procedure = Procedure.objects.get(procedure_name='Leeches',
                                                  procedure_info='have been used for clinical bloodletting for at least 2,500 years')
        self.assertIsNotNone(created_procedure)

    def test_create_new_procedure_missing_name(self):
        request = self.factory.post('create/',
                                    {'notes': 'have been used for clinical bloodletting for at least 2,500 years'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = new_procedure(request)
        self.assertEqual(response.status_code, 401)

        # If an entry exists, it will overwrite None thus failing the test
        try:
            created_procedure = None
            created_procedure = Procedure.objects.get(
                procedure_info='have been used for clinical bloodletting for at least 2,500 years')
        except Procedure.DoesNotExist:
            self.assertIsNone(created_procedure)

    def test_get_procedures(self):
        request = self.factory.get('/procedures/')
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = index(request)
        self.assertEqual(response.status_code, 200)


    def test_get_view_procedure_valid_id(self):
        request = self.factory.get('/procedures/view_procedure/?id=' + str(self.test_procedure.id))
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = view_procedure(request)
        self.assertEqual(response.status_code, 200)

    def test_get_view_procedure_invalid_id(self):
        request = self.factory.get('/procedures/view_procedure/?id=' + str(999999999999) )
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = view_procedure(request)
        self.assertEqual(response.status_code, 302)
