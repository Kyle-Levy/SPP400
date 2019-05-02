from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware

from assigned_procedures.models import AssignedProcedures
from assigned_procedures.views import *
from patients.models import Patients
from patients.views import new_patient, procedures, remove_pairs_from_patient, add_roadmap, add_procedure
from procedures.models import Procedure
from procedures.views import new_procedure
from roadmaps.models import Roadmap
from roadmaps.views import create_roadmap, view_roadmap, add_to_roadmap


class TestRoadmapToPatients(TestCase):
    # create setUp so every test can have access to the requestFactory
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware()
        self.user = User.objects.create_superuser('testuser', 'testuser@email.com', 'super_secret_pass')
        self.user.save()

        # Creating patient for testing the ability to manipulate a patient

        request = self.factory.post('patients/create/',
                                    {'first_name': 'John', 'last_name': 'Smith', 'birth_date': '1950-01-01',
                                     'record_number': '111', 'referring_physician': 'Dr. Who',
                                     'date_of_referral': '2019-01-01'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()
        new_patient(request)
        self.test_patient = Patients.objects.get(first_name='John', last_name='Smith', bday='1950-01-01')

        # Creating procedures for testing the ability to add them to a roadmap
        request = self.factory.post('/procedures/create/', {'procedure_name': 'Object One', 'notes': 'These are test notes', 'time_frame': 'days', 'time': '22'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        new_procedure(request)
        self.test_object_one = Procedure.objects.get(procedure_name='Object One',
                                                     procedure_info='These are test notes')

        # Creating procedures for testing the ability to add them to a roadmap
        request = self.factory.post('/procedures/create/', {'procedure_name': 'Object Two', 'notes': 'These are test notes', 'time_frame': 'days', 'time': '22'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        new_procedure(request)
        self.test_object_two = Procedure.objects.get(procedure_name='Object Two',
                                                     procedure_info='These are test notes')

        # Creating procedures for testing the ability to add them to a roadmap
        request = self.factory.post('/procedures/create/', {'procedure_name': 'Object Three', 'notes': 'These are test notes', 'time_frame': 'days', 'time': '22'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        new_procedure(request)
        self.test_object_three = Procedure.objects.get(procedure_name='Object Three',
                                                       procedure_info='These are test notes')

        request = self.factory.post('/roadmaps/create/', {'roadmap_name': 'Test Roadmap', 'time_frame': 'days', 'time': '22'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        create_roadmap(request)
        self.test_roadmap = Roadmap.objects.get(roadmap_name='Test Roadmap')
        # Done creating procedures and roadmaps

        # View roadmap first
        view_request = self.factory.post('/roadmaps/view_roadmap/?id=' + str(self.test_roadmap.id))
        view_request.user = self.user
        self.middleware.process_request(view_request)
        view_request.session.save()

        view_roadmap(view_request)

        add_request = self.factory.post('/roadmaps/view_roadmap/add_roadmap/?id=' + str(self.test_roadmap.id), {
            'procedure': [self.test_object_one.id, self.test_object_two.id, self.test_object_three.id], 'phase': 1})

        add_request.user = self.user
        add_request.session = view_request.session

        add_to_roadmap(add_request)

    def test_get_patient_procedure_page_valid(self):
        request = self.factory.get('/patients/profile/procedures/?id=' + str(self.test_patient.id))
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user
        response = procedures(request)
        self.assertEqual(response.status_code, 200)

    def test_get_patient_procedure_page_invalid(self):
        request = self.factory.get('/patients/profile/procedures/?id=' + str(99999))
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = procedures(request)
        self.assertEqual(response.status_code, 302)

    # Test adds a roadmap onto a patient and verifies it added successfully
    def test_post_add_roadmap_valid(self):

        post_request = self.factory.post('/patients/profile/procedures/add_roadmap/?id=' + str(self.test_patient.id),
                                         {'roadmap': [str(self.test_roadmap.id)]})
        self.middleware.process_request(post_request)
        post_request.user = self.user
        response = add_roadmap(post_request)
        self.assertEqual(response.status_code, 302)

        expected_list = [(self.test_object_one, 1), (self.test_object_two, 1), (self.test_object_three, 1)]

        self.assertListEqual(expected_list, AssignedProcedures.get_all_procedures(self.test_patient))

        return post_request

    def test_post_add_roadmap_invalid_roadmap(self):

        post_request = self.factory.post('/patients/profile/procedures/add_roadmap/?id=' + str(self.test_patient.id), {'roadmap': [str(99999)]})
        self.middleware.process_request(post_request)
        post_request.user = self.user

        setattr(post_request, 'session', 'session')
        messages = FallbackStorage(post_request)
        setattr(post_request, '_messages', messages)

        response = add_roadmap(post_request)
        self.assertEqual(response.status_code, 302)

        expected_list = []

        self.assertListEqual(expected_list, AssignedProcedures.get_all_procedures(self.test_patient))

    def test_post_add_roadmap_invalid_patient_id(self):
        post_request = self.factory.post('/patients/profile/procedures/add_roadmap/?id=' + str(99999),
                                         {'roadmap': [self.test_roadmap.id]})
        self.middleware.process_request(post_request)

        post_request.user = self.user

        setattr(post_request, 'session', 'session')
        messages = FallbackStorage(post_request)
        setattr(post_request, '_messages', messages)

        response = add_roadmap(post_request)
        self.assertEqual(response.status_code, 302)

        expected_list = []

        self.assertListEqual(expected_list, AssignedProcedures.get_all_procedures(self.test_patient))

    def test_post_add_procedure_valid(self):
        add_request = self.factory.post('profile/procedures/add_procedure/?id=' + str(self.test_patient.id), {
            'procedure': [self.test_object_one.id, self.test_object_two.id, self.test_object_three.id], 'phase': 1})
        self.middleware.process_request(add_request)
        add_request.user = self.user

        response = add_procedure(add_request)
        self.assertEqual(response.status_code, 302)

        expected_list = [(self.test_object_one, 1), (self.test_object_two, 1), (self.test_object_three, 1)]

        self.assertListEqual(expected_list, AssignedProcedures.get_all_procedures(self.test_patient))

    def test_post_add_procedure_invalid_procedure_id(self):
        add_request = self.factory.post('profile/procedures/add_procedure/?id=' + str(self.test_patient.id), {
            'procedure': [99999], 'phase': 1})
        self.middleware.process_request(add_request)
        add_request.user = self.user

        setattr(add_request, 'session', 'session')
        messages = FallbackStorage(add_request)
        setattr(add_request, '_messages', messages)

        response = add_procedure(add_request)
        self.assertEqual(response.status_code, 302)

        expected_list = []

        self.assertListEqual(expected_list, AssignedProcedures.get_all_procedures(self.test_patient))

    def test_post_add_procedure_invalid_patient_id(self):
        add_request = self.factory.post('profile/procedures/add_procedure/?id=' + str(99999), {
            'procedure': [self.test_object_one.id, self.test_object_two.id, self.test_object_three.id], 'phase': 1})
        self.middleware.process_request(add_request)
        add_request.user = self.user

        setattr(add_request, 'session', 'session')
        messages = FallbackStorage(add_request)
        setattr(add_request, '_messages', messages)

        response = add_procedure(add_request)
        self.assertEqual(response.status_code, 302)

        expected_list = []

        self.assertListEqual(expected_list, AssignedProcedures.get_all_procedures(self.test_patient))

    def test_post_remove_procedures(self):
        self.test_post_add_procedure_valid()
        remove_request = self.factory.post('/patients/profile/procedures/remove/?id=' + str(self.test_patient.id), {
            'selection[]': ['1,1', '3,1']
        })
        self.middleware.process_request(remove_request)
        remove_request.user = self.user
        self.middleware.process_request(remove_request)
        response = remove_pairs_from_patient(remove_request)

        self.assertEqual(response.status_code, 302)

        expected_list = [(self.test_object_two, 1)]

        self.assertListEqual(expected_list, AssignedProcedures.get_all_procedures(self.test_patient))

    def test_post_remove_no_procedures(self):
        self.test_post_add_procedure_valid()
        remove_request = self.factory.post('/patients/profile/procedures/remove/?id=' + str(self.test_patient.id), {
            'selection[]': []
        })
        self.middleware.process_request(remove_request)
        remove_request.user = self.user
        self.middleware.process_request(remove_request)
        response = remove_pairs_from_patient(remove_request)

        self.assertEqual(response.status_code, 302)

        expected_list = [(self.test_object_one, 1), (self.test_object_two, 1), (self.test_object_three, 1)]

        self.assertListEqual(expected_list, AssignedProcedures.get_all_procedures(self.test_patient))

    def test_post_remove_procedures_invalid_patient(self):
        self.test_post_add_procedure_valid()
        remove_request = self.factory.post('/patients/profile/procedures/remove/?id=' + str(99999), {
            'selection[]': ['1,1', '3,1']
        })
        self.middleware.process_request(remove_request)
        remove_request.user = self.user
        self.middleware.process_request(remove_request)

        setattr(remove_request, 'session', 'session')
        messages = FallbackStorage(remove_request)
        setattr(remove_request, '_messages', messages)

        response = remove_pairs_from_patient(remove_request)

        self.assertEqual(response.status_code, 302)

        expected_list = [(self.test_object_one, 1), (self.test_object_two, 1), (self.test_object_three, 1)]

        self.assertListEqual(expected_list, AssignedProcedures.get_all_procedures(self.test_patient))

    def test_fail_get_update_page(self):
        request = self.factory.get('/assigned/procedure/?id=134512342344')
        self.middleware.process_request(request)

        request.session.save()
        request.user = self.user

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = update(request)
        self.assertEqual(response.status_code, 302)

    def test_get_update_page(self):
        procedure = AssignedProcedures.assign_procedure_to_patient(1, self.test_patient, self.test_object_one)
        request = self.factory.get('/assigned/procedure/?id=' + str(procedure.id))
        self.middleware.process_request(request)

        request.session.save()
        request.user = self.user

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = update(request)
        self.assertEqual(response.status_code, 200)
