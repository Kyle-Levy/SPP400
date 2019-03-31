from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware

from .views import index, new_patient, profile, update, delete
from .models import Patients


# Create your tests here.
class TestCreatePatient(TestCase):
    # create setUp so every test can have access to the requestFactory
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware()
        self.user = User.objects.create_superuser('testuser', 'testuser@email.com', 'super_secret_pass')
        self.user.save()

        # Creating patient for testing the ability to manipulate a patient

        request = self.factory.post('patients/create/',
                                    {'first_name': 'John', 'last_name': 'Smith', 'birth_date': '1950-01-01',
                                     'record_number': '111', 'referring_physician': 'Dr. Who', 'date_of_referral': '01/01/2019'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()
        new_patient(request)
        self.test_patient = Patients.objects.get(first_name='John', last_name='Smith', bday='1950-01-01')

    def test_valid_patient(self):

        request = self.factory.post('patients/create/',
                                    {'first_name': 'Marie', 'last_name': 'Smith', 'birth_date': '1950-02-01', 'record_number': '112', 'referring_physician': 'Dr. Who', 'date_of_referral': '01/01/2019'})
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        response = new_patient(request)

        self.assertEqual(response.status_code, 302)

        # If the patient does exist, the value of None will be overwritten

        created_patient = Patients.objects.get(first_name='Marie', last_name='Smith', bday='1950-02-01')

        self.assertIsNotNone(created_patient)

    def test_missing_first_name(self):

        request = self.factory.post('patients/create/', {'last_name': 'Smith', 'birth_date': '1950-02-01', 'record_number': '111', 'referring_physician': 'Dr. Who', 'date_of_referral': '01/01/2019'})
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        response = new_patient(request)

        self.assertEqual(response.status_code, 401)

    def test_missing_last_name(self):

        request = self.factory.post('patients/create/', {'first_name': 'Marie', 'birth_date': '1950-02-01', 'record_number': '111', 'referring_physician': 'Dr. Who', 'date_of_referral': '01/01/2019'})
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        response = new_patient(request)

        self.assertEqual(response.status_code, 401)

    def test_missing_bday(self):

        request = self.factory.post('patients/create/', {'first_name': 'Marie', 'last_name': 'Smith', 'record_number': '111', 'referring_physician': 'Dr. Who', 'date_of_referral': '01/01/2019'})
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        response = new_patient(request)

        self.assertEqual(response.status_code, 401)

    def test_missing_mrn(self):

        request = self.factory.post('patients/create/',
                                    {'first_name': 'Marie', 'last_name': 'Smith', 'birth_date': '1950-02-01', 'referring_physician': 'Dr. Who', 'date_of_referral': '01/01/2019'})
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        response = new_patient(request)

        self.assertEqual(response.status_code, 401)

    def test_missing_referring_physician(self):

        request = self.factory.post('patients/create/',
                                    {'first_name': 'Marie', 'last_name': 'Smith', 'birth_date': '1950-02-01',
                                     'record_number': '112', 'date_of_referral': '01/01/2019'})
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        response = new_patient(request)

        self.assertEqual(response.status_code, 401)

    def test_missing_date_of_referral(self):

        request = self.factory.post('patients/create/',
                                    {'first_name': 'Marie', 'last_name': 'Smith', 'birth_date': '1950-02-01',
                                     'record_number': '112', 'referring_physician': 'Dr. Who'})
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        response = new_patient(request)

        self.assertEqual(response.status_code, 401)

    def test_get_patients(self):
        request = self.factory.get('/patients/')

        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        response = index(request)

        self.assertEqual(response.status_code, 200)

    def test_get_new_patients(self):
        request = self.factory.get('/patients/create/')

        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        response = new_patient(request)

        self.assertEqual(response.status_code, 200)

    def test_get_profile_valid_id(self):
        request = self.factory.get('/patients/profile/?id=' + str(self.test_patient.id))
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = profile(request)
        self.assertEqual(response.status_code, 200)

    def test_get_view_procedure_invalid_id(self):
        request = self.factory.get('/patients/profile/?id=' + str(999999999999))
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = profile(request)
        self.assertEqual(response.status_code, 302)

    def test_post_view_procedure_valid_id(self):
        request = self.factory.post('/patients/profile/?id=' + str(self.test_patient.id))
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = profile(request)
        self.assertEqual(response.status_code, 200)

    def test_post_view_procedure_invalid_id(self):
        request = self.factory.post('/patients/profile/?id=' + str(99999))
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = profile(request)
        self.assertEqual(response.status_code, 302)

    def test_post_update_patient_valid_id(self):
        profile_request = self.factory.post('/patients/profile/?id=' + str(self.test_patient.id))
        profile_request.user = self.user
        self.middleware.process_request(profile_request)
        profile_request.session.save()

        profile(profile_request)

        request = self.factory.post('/patients/profile/update',
                                    {'first_name': 'Bill', 'last_name': 'Jobs', 'record_number': 'a',
                                     'birth_date': '2000-03-03', 'referring_physician': 'Dr. Seuss', 'date_of_referral': '02/02/2019'})
        request.user = self.user
        request.session = profile_request.session
        request.session.save()

        response = update(request)

        self.assertEqual(response.status_code, 302)

        updated_patient = Patients.objects.get(first_name='Bill', last_name='Jobs', bday='2000-03-03')
        self.assertIsNotNone(updated_patient)

    def test_post_update_patient_invalid_id(self):
        profile_request = self.factory.post('/patients/profile/?id=' + str(self.test_patient.id))
        profile_request.user = self.user
        self.middleware.process_request(profile_request)
        profile_request.session.save()

        profile(profile_request)

        request = self.factory.post('/patients/profile/update',
                                    {'first_name': 'Bill', 'last_name': 'Jobs', 'record_number': 'a',
                                     'birth_date': '2000-03-03', 'referring_physician': 'Dr. Seuss', 'date_of_referral': '02/02/2019'})
        request.user = self.user
        request.session = profile_request.session
        request.session.save()

        # Fudge the id
        request.session['patient_id'] = 9999999
        request.session.save()

        response = update(request)

        self.assertEqual(response.status_code, 302)

        # If an entry exists, it will overwrite None, thus failing the test
        try:
            updated_patient = None
            updated_patient = Patients.objects.get(first_name='Bill', last_name='Jobs', bday='2000-03-03')
        except Patients.DoesNotExist:
            self.assertIsNone(updated_patient)

    def test_post_update_patient_invalid_form(self):
        profile_request = self.factory.post('/patients/profile/?id=' + str(self.test_patient.id))
        profile_request.user = self.user
        self.middleware.process_request(profile_request)
        profile_request.session.save()

        profile(profile_request)

        request = self.factory.post('/patients/profile/update',
                                    {'first_name': 'Bill', 'record_number': 'a', 'birth_date': '2000-03-03'})
        request.user = self.user
        request.session = profile_request.session
        request.session.save()

        response = update(request)

        self.assertEqual(response.status_code, 401)

        # If an entry exists, it will overwrite None, thus failing the test
        try:
            updated_patient = None
            updated_patient = Patients.objects.get(first_name='Bill', last_name='Jobs', bday='2000-03-03')
        except Patients.DoesNotExist:
            self.assertIsNone(updated_patient)

    def test_post_delete_patient_valid_id(self):
        profile_request = self.factory.post('/patients/profile/?id=' + str(self.test_patient.id))
        profile_request.user = self.user
        self.middleware.process_request(profile_request)
        profile_request.session.save()

        profile(profile_request)

        request = self.factory.post('/patients/profile/delete')
        request.user = self.user
        request.session = profile_request.session
        request.session.save()

        response = delete(request)

        self.assertEqual(response.status_code, 302)

        # If an entry exists, it will overwrite None, thus failing the test
        try:
            updated_patient = None
            updated_patient = Patients.objects.get(first_name='John', last_name='Smith', bday='1950-01-01')
        except Patients.DoesNotExist:
            self.assertIsNone(updated_patient)

    def test_post_delete_patient_invalid_id(self):
        profile_request = self.factory.post('/patients/profile/?id=' + str(self.test_patient.id))
        profile_request.user = self.user
        self.middleware.process_request(profile_request)
        profile_request.session.save()

        profile(profile_request)

        request = self.factory.post('/patients/profile/delete')
        request.user = self.user
        request.session = profile_request.session
        request.session.save()

        # Fudge the id
        request.session['patient_id'] = 9999999
        request.session.save()

        response = delete(request)

        self.assertEqual(response.status_code, 302)

        # If an entry exists, it will overwrite None, thus failing the test

        updated_patient = Patients.objects.get(first_name='John', last_name='Smith', bday='1950-01-01')
        self.assertIsNotNone(updated_patient)

    def test_search_patients(self):
        request = self.factory.post('/patients/', {'search_terms': 'john'})
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user
        response = index(request)
        self.assertEqual(response.status_code, 200)


'''
#If the patient does exist, the value of None will be overwritten.
        try:
            created_patient = None;
            created_patient = Patients.objects.get(first_name='John', last_name='Smith', bday='1950-02-01')
        except Patients.DoesNotExist:
            self.assertIsNone(created_patient)
'''
