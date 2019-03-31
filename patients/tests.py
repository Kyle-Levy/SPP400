from django.test import TestCase
from patients import models
from patients.models import Patients
from datetime import date
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
import pytz


# Create your tests here.
class TestPatientModel(TestCase):

    def create_patient(self, first_name="Kyle", last_name="Dorcey", bday=datetime(1996, 10, 24), doc_notes="he sick",
                       referring_physician='Dr. Seuss', date_of_referral='01/01/2019'):
        return Patients.objects.create(first_name=first_name, last_name=last_name, bday=bday,
                                       referring_physician=referring_physician, date_of_referral=date_of_referral,
                                       doc_notes=doc_notes, flagged=False, patient_flagged_reason="none",
                                       today_flag=False, today_flag_end=timezone.now(), today_flag_reason="")

    def test_enableTodayFlag(self):
        test_patient = self.create_patient()
        flag_expiration = timezone.now() + timedelta(days=1)
        test_patient.toggle_today_flag()
        self.assertEqual(test_patient.today_flag, True)
        self.assertEqual(test_patient.today_flag_end.day, flag_expiration.day)

    def test_disableTodayFlag(self):
        test_patient = self.create_patient()
        test_patient.today_flag = True
        test_patient.today_flag_end = timezone.now() + timedelta(days=1)
        self.assertEqual(test_patient.toggle_today_flag(), False)
        self.assertEqual(test_patient.today_flag_end, None)

    def test_today_flag_expired(self):
        test_patient = self.create_patient()
        test_patient.today_flag = True
        test_patient.today_flag_end = timezone.now() - timedelta(days=1)
        self.assertEqual(test_patient.check_today_flag(), False)

    def test_flagged_toggle(self):
        test_patient = self.create_patient()
        test_patient.flagged = True
        test_patient.toggle_flag()
        self.assertEqual(test_patient.flagged, False)
