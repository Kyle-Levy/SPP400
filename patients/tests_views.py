from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware

from .views import *
from .models import Patients
from django.contrib.messages.storage.fallback import FallbackStorage

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
                                     'record_number': '111', 'referring_physician': 'Dr. Who', 'date_of_referral': '2019-01-01'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()
        new_patient(request)
        self.test_patient = Patients.objects.get(first_name='John', last_name='Smith', bday='1950-01-01')

    def test_create_valid_patient(self):

        request = self.factory.post('patients/create/',
                                    {'first_name': 'Marie', 'last_name': 'Smith', 'birth_date': '1950-02-01', 'record_number': '112', 'referring_physician': 'Dr. Who', 'date_of_referral': '2019-01-01'})
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        response = new_patient(request)

        self.assertEqual(response.status_code, 302)

        # If the patient does exist, the value of None will be overwritten

        created_patient = Patients.objects.get(first_name='Marie', last_name='Smith', bday='1950-02-01')

        self.assertIsNotNone(created_patient)

    def test_missing_first_name(self):

        request = self.factory.post('patients/create/', {'last_name': 'Smith', 'birth_date': '1950-02-01', 'record_number': '111', 'referring_physician': 'Dr. Who', 'date_of_referral': '2019-01-01'})
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = new_patient(request)

        self.assertEqual(response.status_code, 302)

    def test_missing_last_name(self):

        request = self.factory.post('patients/create/', {'first_name': 'Marie', 'birth_date': '1950-02-01', 'record_number': '111', 'referring_physician': 'Dr. Who', 'date_of_referral': '2019-01-01'})
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = new_patient(request)

        self.assertEqual(response.status_code, 302)

    def test_missing_bday(self):

        request = self.factory.post('patients/create/', {'first_name': 'Marie', 'last_name': 'Smith', 'record_number': '111', 'referring_physician': 'Dr. Who', 'date_of_referral': '2019-01-01'})
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = new_patient(request)

        self.assertEqual(response.status_code, 302)

    def test_missing_mrn(self):

        request = self.factory.post('patients/create/',
                                    {'first_name': 'Marie', 'last_name': 'Smith', 'birth_date': '1950-02-01', 'referring_physician': 'Dr. Who', 'date_of_referral': '2019-01-01'})
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = new_patient(request)

        self.assertEqual(response.status_code, 302)

    def test_missing_referring_physician(self):

        request = self.factory.post('patients/create/',
                                    {'first_name': 'Marie', 'last_name': 'Smith', 'birth_date': '1950-02-01',
                                     'record_number': '112', 'date_of_referral': '2019-01-01'})
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = new_patient(request)

        self.assertEqual(response.status_code, 302)

    def test_missing_date_of_referral(self):

        request = self.factory.post('patients/create/',
                                    {'first_name': 'Marie', 'last_name': 'Smith', 'birth_date': '1950-02-01',
                                     'record_number': '112', 'referring_physician': 'Dr. Who'})
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = new_patient(request)

        self.assertEqual(response.status_code, 302)

#####################################################################################################

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

    def test_get_view_profile_invalid_id(self):
        request = self.factory.get('/patients/profile/?id=' + str(999999999999))
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = profile(request)
        self.assertEqual(response.status_code, 302)


    def test_get_update_page_valid_id(self):
        request = self.factory.get('/patients/profile/update/?id=' + str(self.test_patient.id))
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = update(request)
        self.assertEqual(response.status_code, 200)

    def test_get_update_page_invalid_id(self):
        request = self.factory.get('/patients/profile/update/?id=' + str(99999))
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = update(request)
        self.assertEqual(response.status_code, 302)

    def test_post_update_patient_valid_id(self):
        request = self.factory.post('/patients/profile/update/?id=' + str(self.test_patient.id),
                                    {'first_name': 'Bill', 'last_name': 'Jobs', 'record_number': 'a',
                                     'birth_date': '2000-03-03', 'referring_physician': 'Dr. Seuss',
                                     'date_of_referral': '02/02/2019'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = update(request)

        self.assertEqual(response.status_code, 302)

        updated_patient = Patients.objects.get(first_name='Bill', last_name='Jobs', bday='2000-03-03')
        self.assertIsNotNone(updated_patient)


    def test_post_update_patient_invalid_id(self):
        request = self.factory.post('/patients/profile/update/?id=' + str(99999),
                                    {'first_name': 'Bill', 'last_name': 'Jobs', 'record_number': 'a',
                                     'birth_date': '2000-03-03', 'referring_physician': 'Dr. Seuss',
                                     'date_of_referral': '02/02/2019'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = update(request)

        self.assertEqual(response.status_code, 302)

        # If an entry exists, it will overwrite None, thus failing the test
        try:
            updated_patient = None
            updated_patient = Patients.objects.get(first_name='Bill', last_name='Jobs', bday='2000-03-03')
        except Patients.DoesNotExist:
            self.assertIsNone(updated_patient)


    def test_post_update_patient_invalid_form(self):
        request = self.factory.post('/patients/profile/update/?id=' + str(self.test_patient.id),
                                    {'first_name': 'Bill', 'record_number': 'a', 'birth_date': '2000'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        # This unit tests encounters a bug in django with the messages app, so this must be done as a way to mock messages
        # https://stackoverflow.com/questions/11938164/why-dont-my-django-unittests-know-that-messagemiddleware-is-installed
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = update(request)

        self.assertEqual(response.status_code, 302)

        # If an entry exists, it will overwrite None, thus failing the test
        try:
            updated_patient = None
            updated_patient = Patients.objects.get(first_name='Bill', last_name='Jobs', bday='2000-03-03')
        except Patients.DoesNotExist:
            self.assertIsNone(updated_patient)


    def test_post_delete_patient_valid_id(self):
        request = self.factory.post('/patients/profile/delete/?id=' + str(self.test_patient.id), {'item_name': str(self.test_patient.record_number)})
        request.user = self.user
        self.middleware.process_request(request)
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
        request = self.factory.post('/patients/profile/delete/?id=' + str(99999), {'item_name': str(self.test_patient.record_number)})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = delete(request)

        self.assertEqual(response.status_code, 302)

        # If an entry exists, it will overwrite None, thus failing the test

        updated_patient = Patients.objects.get(first_name='John', last_name='Smith', bday='1950-01-01')
        self.assertIsNotNone(updated_patient)

    def test_post_delete_patient_invalid_record_number(self):
        request = self.factory.post('/patients/profile/delete/?id=' + str(self.test_patient.id), {'item_name': str(self.test_patient.record_number + "99999")})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = delete(request)

        self.assertEqual(response.status_code, 302)

        # If an entry exists, it will overwrite None, thus failing the test

        updated_patient = Patients.objects.get(first_name='John', last_name='Smith', bday='1950-01-01')
        self.assertIsNotNone(updated_patient)

    def test_post_delete_patient_missing_record_number(self):
        request = self.factory.post('/patients/profile/delete/?id=' + str(self.test_patient.id), {})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

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

    def test_valid_flag_patient(self):
        request = self.factory.post('/patients/profile/flag/?id=' + str(self.test_patient.id),
                                    {'notes': "Didn't respond to emails."})
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user
        response = flag_patient(request)
        modified_patient = Patients.objects.get(first_name='John', last_name='Smith', bday='1950-01-01')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(modified_patient.flagged)
        self.assertEqual(modified_patient.patient_flagged_reason, "Didn't respond to emails.")

    def test_invalid_notes(self):
        request = self.factory.post('/patients/profile/flag/?id=' + str(self.test_patient.id), {'notes': ""})
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = flag_patient(request)

        modified_patient = Patients.objects.get(first_name='John', last_name='Smith', bday='1950-01-01')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(modified_patient.flagged)
        self.assertEqual(modified_patient.patient_flagged_reason, "")

    def test_invalid_id_flag_patient(self):
        request = self.factory.post('/patients/profile/flag/?id=' + str(99999), {'notes': "Didn't respond to emails."})
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = flag_patient(request)
        self.assertEqual(response.status_code, 302)

    def test_valid_unflagged_patient(self):
        self.test_valid_flag_patient()
        request = self.factory.post('/patients/profile/unflag/?id=' + str(self.test_patient.id))
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user
        response = unflag_patient(request)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.test_patient.flagged)
        self.assertEqual(self.test_patient.patient_flagged_reason, '')

    def test_invalid_id_unflagged_patient(self):
        self.test_valid_flag_patient()
        request = self.factory.post('/patients/profile/unflag/?id=' + str(99999))
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = unflag_patient(request)
        self.assertEqual(response.status_code, 302)

    def test_get_procedures_page_valid_id(self):
        request = self.factory.get('/patients/profile/procedures/?id=' + str(self.test_patient.id))
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        response = procedures(request)

        self.assertEqual(response.status_code, 200)

    def test_get_procedures_page_invalid_id(self):
        request = self.factory.get('/patients/profile/procedures/?id=' + str(99999))
        self.middleware.process_request(request)
        request.session.save()
        request.user = self.user

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = procedures(request)

        self.assertEqual(response.status_code, 302)


