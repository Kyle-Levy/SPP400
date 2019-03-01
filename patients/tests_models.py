from django.test import TestCase
from patients.models import Patients


class TestPatientsModel(TestCase):

    def create_patient(self, first_name='Steve', last_name='Stevens', bday='2000-01-01'):
        return Patients.objects.create(first_name=first_name, last_name=last_name, bday=bday)

    def test_str(self):
        test_patient = self.create_patient()

        self.assertEqual(str(test_patient), 'Steve Stevens')
