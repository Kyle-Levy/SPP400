from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware

from assigned_procedures.models import AssignedProcedures
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
        request = self.factory.post('create/', {'procedure_name': 'Object One', 'notes': 'These are test notes'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        new_procedure(request)
        self.test_object_one = Procedure.objects.get(procedure_name='Object One',
                                                     procedure_info='These are test notes')

        # Creating procedures for testing the ability to add them to a roadmap
        request = self.factory.post('create/', {'procedure_name': 'Object Two', 'notes': 'These are test notes'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        new_procedure(request)
        self.test_object_two = Procedure.objects.get(procedure_name='Object Two',
                                                     procedure_info='These are test notes')

        # Creating procedures for testing the ability to add them to a roadmap
        request = self.factory.post('create/', {'procedure_name': 'Object Three', 'notes': 'These are test notes'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        new_procedure(request)
        self.test_object_three = Procedure.objects.get(procedure_name='Object Three',
                                                       procedure_info='These are test notes')

        request = self.factory.post('/roadmaps/create/', {'roadmap_name': 'Test Roadmap'})
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

        add_request = self.factory.post('/roadmaps/view_roadmap/add/', {
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
        response = procedures(request)
        self.assertEqual(response.status_code, 302)

    # Test adds a roadmap onto a patient and verifies it added successfully
    def test_post_patient_procedure_valid(self):
        # Need to get the previous page to store id in session
        get_request = self.factory.get('/patients/profile/procedures/?id=' + str(self.test_patient.id))
        self.middleware.process_request(get_request)
        get_request.session.save()
        get_request.user = self.user
        response = procedures(get_request)
        self.assertEqual(response.status_code, 200)

        post_request = self.factory.post('/patients/profile/procedures/add_roadmap/',
                                         {'roadmap': [str(self.test_roadmap.id)]})
        self.middleware.process_request(post_request)
        post_request.session = get_request.session
        post_request.user = self.user
        response = add_roadmap(post_request)
        self.assertEqual(response.status_code, 302)

        expected_list = [(self.test_object_one, 1), (self.test_object_two, 1), (self.test_object_three, 1)]

        self.assertListEqual(expected_list, AssignedProcedures.get_all_procedures(self.test_patient))

        return post_request

    def test_post_patient_procedure_invalid_roadmap(self):
        # Need to get the previous page to store id in session
        get_request = self.factory.get('/patients/profile/procedures/?id=' + str(self.test_patient.id))
        self.middleware.process_request(get_request)
        get_request.session.save()
        get_request.user = self.user
        response = procedures(get_request)
        self.assertEqual(response.status_code, 200)

        post_request = self.factory.post('/patients/profile/procedures/add_roadmap/', {'roadmap': [str(99999)]})
        self.middleware.process_request(post_request)
        post_request.session = get_request.session
        post_request.user = self.user
        response = add_roadmap(post_request)
        self.assertEqual(response.status_code, 302)

        expected_list = []

        self.assertListEqual(expected_list, AssignedProcedures.get_all_procedures(self.test_patient))

    def test_post_patient_procedure_invalid_patient_id(self):
        # Need to get the previous page to store id in session
        get_request = self.factory.get('/patients/profile/procedures/?id=' + str(self.test_patient.id))
        self.middleware.process_request(get_request)
        get_request.session.save()
        get_request.user = self.user
        response = procedures(get_request)
        self.assertEqual(response.status_code, 200)

        post_request = self.factory.post('/patients/profile/procedures/add_roadmap/',
                                         {'roadmap': [self.test_roadmap.id]})
        self.middleware.process_request(post_request)
        post_request.session = get_request.session

        post_request.session['patient_id'] = 99999
        post_request.user = self.user
        response = add_roadmap(post_request)
        self.assertEqual(response.status_code, 302)

        expected_list = []

        self.assertListEqual(expected_list, AssignedProcedures.get_all_procedures(self.test_patient))

    def test_post_add_procedure_valid(self):
        # Need to get the previous page to store id in session
        get_request = self.factory.get('/patients/profile/procedures/?id=' + str(self.test_patient.id))
        self.middleware.process_request(get_request)
        get_request.session.save()
        get_request.user = self.user
        response = procedures(get_request)
        self.assertEqual(response.status_code, 200)

        expected_list = []

        self.assertListEqual(expected_list, AssignedProcedures.get_all_procedures(self.test_patient))

        add_request = self.factory.post('profile/procedures/add_procedure/', {
            'procedure': [self.test_object_one.id, self.test_object_two.id, self.test_object_three.id], 'phase': 1})
        add_request.session = get_request.session
        add_request.user = self.user
        response = add_procedure(add_request)
        self.assertEqual(response.status_code, 302)

        expected_list = [(self.test_object_one, 1), (self.test_object_two, 1),(self.test_object_three, 1)]

        self.assertListEqual(expected_list, AssignedProcedures.get_all_procedures(self.test_patient))

    def test_post_add_procedure_invalid_procedure_id(self):
        # Need to get the previous page to store id in session
        get_request = self.factory.get('/patients/profile/procedures/?id=' + str(self.test_patient.id))
        self.middleware.process_request(get_request)
        get_request.session.save()
        get_request.user = self.user
        response = procedures(get_request)
        self.assertEqual(response.status_code, 200)

        expected_list = []

        self.assertListEqual(expected_list, AssignedProcedures.get_all_procedures(self.test_patient))

        add_request = self.factory.post('profile/procedures/add_procedure/', {
            'procedure': [99999], 'phase': 1})
        add_request.session = get_request.session
        add_request.user = self.user
        response = add_procedure(add_request)
        self.assertEqual(response.status_code, 302)

        expected_list = []

        self.assertListEqual(expected_list, AssignedProcedures.get_all_procedures(self.test_patient))

    def test_post_add_procedure_invalid_patient_id(self):
        # Need to get the previous page to store id in session
        get_request = self.factory.get('/patients/profile/procedures/?id=' + str(self.test_patient.id))
        self.middleware.process_request(get_request)
        get_request.session.save()
        get_request.user = self.user
        response = procedures(get_request)
        self.assertEqual(response.status_code, 200)

        expected_list = []

        self.assertListEqual(expected_list, AssignedProcedures.get_all_procedures(self.test_patient))

        add_request = self.factory.post('profile/procedures/add_procedure/', {
            'procedure': [self.test_object_one.id, self.test_object_two.id, self.test_object_three.id], 'phase': 1})
        add_request.session = get_request.session
        add_request.user = self.user
        add_request.session['patient_id'] = 99999
        response = add_procedure(add_request)
        self.assertEqual(response.status_code, 302)

        expected_list = []

        self.assertListEqual(expected_list, AssignedProcedures.get_all_procedures(self.test_patient))



    def test_post_remove_procedures(self):
        add_request = self.test_post_patient_procedure_valid()
        remove_request = self.factory.post('/patients/profile/procedures/remove/', {
            'selection[]': ['1,1', '3,1']
        })
        self.middleware.process_request(remove_request)
        remove_request.user = self.user
        remove_request.session = add_request.session
        response = remove_pairs_from_patient(remove_request)

        self.assertEqual(response.status_code, 302)

        expected_list = [(self.test_object_two, 1)]

        self.assertListEqual(expected_list, AssignedProcedures.get_all_procedures(self.test_patient))

    def test_post_remove_procedures_invalid_patient(self):
        add_request = self.test_post_patient_procedure_valid()
        remove_request = self.factory.post('/patients/profile/procedures/remove/', {
            'selection[]': ['1,1', '3,1']
        })
        self.middleware.process_request(remove_request)
        remove_request.user = self.user
        remove_request.session = add_request.session
        remove_request.session['patient_id'] = 99999
        response = remove_pairs_from_patient(remove_request)

        self.assertEqual(response.status_code, 302)

        expected_list = [(self.test_object_one, 1), (self.test_object_two, 1), (self.test_object_three, 1)]

        self.assertListEqual(expected_list, AssignedProcedures.get_all_procedures(self.test_patient))
