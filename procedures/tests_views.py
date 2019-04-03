from django.test import RequestFactory, TestCase
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User
from procedures.views import index, new_procedure, view_procedure, update_procedure, delete_this_procedure
from .models import Procedure


class TestProcedures(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware()
        self.user = User.objects.create_superuser('testuser', 'testuser@email.com', 'supersecretpass')
        self.user.save()

        # Creating procedure for testing the ability to manipulate a procedure
        request = self.factory.post('procedures/create/', {'procedure_name': 'View Procedure', 'notes': 'These are test notes', 'time_frame': 'days', 'time': '22'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()
        new_procedure(request)
        self.test_procedure = Procedure.objects.get(procedure_name='View Procedure',
                                                    procedure_info='These are test notes')

    def test_create_new_procedure(self):
        request = self.factory.post('procedures/create/', {'procedure_name': 'Leeches',
                                        'notes': 'have been used for clinical bloodletting for at least 2,500 years',
                                        'time_frame': 'days', 'time': '22'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = new_procedure(request)
        self.assertEqual(response.status_code, 302)

        created_procedure = Procedure.objects.get(procedure_name='Leeches',
                                                  procedure_info='have been used for clinical bloodletting for at least 2,500 years')
        self.assertIsNotNone(created_procedure)

    def test_create_new_procedure_missing_name(self):
        request = self.factory.post('procedures/create/',
                                    {'notes': 'have been used for clinical bloodletting for at least 2,500 years'
                                        , 'time_frame': 'days', 'time': '22'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = new_procedure(request)
        self.assertEqual(response.status_code, 401)

        # If an entry exists, it will overwrite None, thus failing the test
        try:
            created_procedure = None
            created_procedure = Procedure.objects.get(
                procedure_info='have been used for clinical bloodletting for at least 2,500 years')
        except Procedure.DoesNotExist:
            self.assertIsNone(created_procedure)

    def test_new_procedures(self):
        request = self.factory.get('/procedures/create')
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = new_procedure(request)
        self.assertEqual(response.status_code, 200)

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
        request = self.factory.get('/procedures/view_procedure/?id=' + str(999999999999))
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = view_procedure(request)
        self.assertEqual(response.status_code, 302)

    def test_post_view_procedure_valid_id(self):
        request = self.factory.post('/procedures/view_procedure/?id=' + str(self.test_procedure.id))
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = view_procedure(request)
        self.assertEqual(response.status_code, 200)

    def test_post_view_procedure_invalid_id(self):
        request = self.factory.post('/procedures/view_procedure/?id=' + str(99999))
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = view_procedure(request)
        self.assertEqual(response.status_code, 302)

    def test_post_update_procedure_valid_id(self):
        view_request = self.factory.post('/procedures/view_procedure/?id=' + str(self.test_procedure.id))
        view_request.user = self.user
        self.middleware.process_request(view_request)
        view_request.session.save()

        view_procedure(view_request)

        request = self.factory.post('/procedures/view_procedure/update',
                                    {'procedure_name': 'Updated Procedure', 'notes': 'Updated Procedure Info'
                                        , 'time_frame': 'days', 'time': '22'})
        request.user = self.user
        request.session = view_request.session
        request.session.save()

        response = update_procedure(request)

        self.assertEqual(response.status_code, 302)

        updated_procedure = Procedure.objects.get(procedure_name='Updated Procedure',
                                                  procedure_info='Updated Procedure Info')
        self.assertIsNotNone(updated_procedure)

    def test_post_update_procedure_invalid_id(self):
        view_request = self.factory.post('/procedures/view_procedure/?id=' + str(self.test_procedure.id))
        view_request.user = self.user
        self.middleware.process_request(view_request)
        view_request.session.save()

        view_procedure(view_request)

        request = self.factory.post('/procedures/view_procedure/update',
                                    {'procedure_name': 'Updated Procedure', 'notes': 'Updated Procedure Info',
                                     'time_frame': 'days', 'time': '22'})
        request.user = self.user
        request.session = view_request.session
        request.session.save()

        # Fudge the id
        request.session['procedure_id'] = 9999999
        request.session.save()

        response = update_procedure(request)

        self.assertEqual(response.status_code, 302)

        # If an entry exists, it will overwrite None, thus failing the test
        try:
            updated_procedure = None
            updated_procedure = Procedure.objects.get(procedure_name='Updated Procedure',
                                                      procedure_info='Updated Procedure Info')
        except Procedure.DoesNotExist:
            self.assertIsNone(updated_procedure)

    def test_post_update_procedure_invalid_form(self):
        view_request = self.factory.post('/procedures/view_procedure/?id=' + str(self.test_procedure.id))
        view_request.user = self.user
        self.middleware.process_request(view_request)
        view_request.session.save()

        view_procedure(view_request)

        request = self.factory.post('/procedures/view_procedure/update', {'notes': 'Updated Procedure Info'})
        request.user = self.user
        request.session = view_request.session
        request.session.save()

        response = update_procedure(request)

        self.assertEqual(response.status_code, 401)

        # If an entry exists, it will overwrite None, thus failing the test
        try:
            updated_procedure = None
            updated_procedure = Procedure.objects.get(procedure_info='Updated Procedure Info')
        except Procedure.DoesNotExist:
            self.assertIsNone(updated_procedure)

    def test_post_delete_procedure_valid_id(self):
        view_request = self.factory.post('/procedures/view_procedure/?id=' + str(self.test_procedure.id))
        view_request.user = self.user
        self.middleware.process_request(view_request)
        view_request.session.save()

        view_procedure(view_request)

        request = self.factory.post('/procedures/view_procedure/delete')
        request.user = self.user
        request.session = view_request.session
        request.session.save()

        response = delete_this_procedure(request)

        self.assertEqual(response.status_code, 302)

        # If an entry exists, it will overwrite None, thus failing the test
        try:
            deleted_procedure = None
            deleted_procedure = Procedure.objects.get(procedure_name='View Procedure',
                                                      procedure_info='These are test notes')
        except Procedure.DoesNotExist:
            self.assertIsNone(deleted_procedure)

    def test_post_delete_procedure_invalid_id(self):
        view_request = self.factory.post('/procedures/view_procedure/?id=' + str(self.test_procedure.id))
        view_request.user = self.user
        self.middleware.process_request(view_request)
        view_request.session.save()

        view_procedure(view_request)

        request = self.factory.post('/procedures/view_procedure/delete')
        request.user = self.user
        request.session = view_request.session
        request.session.save()

        # Fudge the id
        request.session['procedure_id'] = 9999999
        request.session.save()

        response = delete_this_procedure(request)

        self.assertEqual(response.status_code, 302)

        deleted_procedure = Procedure.objects.get(procedure_name='View Procedure',
                                                  procedure_info='These are test notes')
        # deleted_procedure can still be retrieved since the wrong ID was used.
        self.assertIsNotNone(deleted_procedure)

    def test_search_procedures(self):
        request = self.factory.post('/procedures/', {'search_terms': 'john'})
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user
        response = index(request)
        self.assertEqual(response.status_code, 200)
