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
                       referring_physician='Dr. Seuss', date_of_referral='2019-01-01'):
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

    def test_flag_update(self):
        from assigned_procedures.models import AssignedProcedures
        from procedures.models import Procedure

        tProcedure = Procedure.objects.create(procedure_name="leeches")
        tProcedure.save()
        tProcedure2 = Procedure.objects.create(procedure_name="Bloodwork")
        tProcedure2.save()
        tProcedure3 = Procedure.objects.create(procedure_name="TAVR")
        tProcedure3.save()
        tPatient = self.create_patient()
        tPatient.save()

        AssignedProcedures.assign_procedure_to_patient(1,tPatient,tProcedure)
        AssignedProcedures.assign_procedure_to_patient(2,tPatient,tProcedure2)
        AssignedProcedures.assign_procedure_to_patient(3,tPatient,tProcedure3)

        self.assertEqual(tPatient.flag_update(), (None, False))
        tProcedure = Procedure.objects.create(procedure_name="mmmhm popy")
        tProcedure.save()
        AssignedProcedures.assign_procedure_to_patient(4, tPatient, tProcedure, -10)
        self.assertEqual(tPatient.flag_update(), (tProcedure, True))

    def test_patient_status(self):
        from assigned_procedures.models import AssignedProcedures
        from procedures.models import Procedure

        tPatient = self.create_patient()
        tPatient.save()

        actualResult = tPatient.patient_status()

        self.assertEqual("Referred", actualResult)

        tProcedure = Procedure.objects.create(procedure_name="leeches")
        tProcedure.save()
        tProcedure2 = Procedure.objects.create(procedure_name="Bloodwork")
        tProcedure2.save()
        tProcedure3 = Procedure.objects.create(procedure_name="TAVR")
        tProcedure3.save()


        ap1 = AssignedProcedures.assign_procedure_to_patient(1,tPatient,tProcedure)
        ap2 = AssignedProcedures.assign_procedure_to_patient(2,tPatient,tProcedure2)
        ap3 = AssignedProcedures.assign_procedure_to_patient(3,tPatient,tProcedure3)

        actualResult = tPatient.patient_status()

        self.assertEqual("In-Progress", actualResult)

        ap1.completed = True
        ap1.save()
        ap2.completed = True
        ap2.save()

        actualResult = tPatient.patient_status()

        self.assertEqual("Ready", actualResult)

        ap3.completed = True
        ap3.save()

        actualResult = tPatient.patient_status()

        self.assertEqual("Done", actualResult)

    def test_patient_final_procedures(self):
        from assigned_procedures.models import AssignedProcedures
        from procedures.models import Procedure

        tPatient = self.create_patient()
        tPatient.save()

        actualResult = tPatient.patient_status()

        self.assertEqual("Referred", actualResult)

        tProcedure = Procedure.objects.create(procedure_name="leeches")
        tProcedure.save()
        tProcedure2 = Procedure.objects.create(procedure_name="Bloodwork")
        tProcedure2.save()
        tProcedure3 = Procedure.objects.create(procedure_name="TAVR")
        tProcedure3.save()


        ap1 = AssignedProcedures.assign_procedure_to_patient(1,tPatient,tProcedure)
        ap2 = AssignedProcedures.assign_procedure_to_patient(2,tPatient,tProcedure2)
        ap3 = AssignedProcedures.assign_procedure_to_patient(3,tPatient,tProcedure3)

        expected_list = [tProcedure3]
        final_procedures_list = tPatient.patient_final_procedures()
        self.assertListEqual(expected_list, final_procedures_list)

    def test_patient_next_procedures(self):
        from assigned_procedures.models import AssignedProcedures
        from procedures.models import Procedure

        tPatient = self.create_patient()
        tPatient.save()

        actualResult = tPatient.patient_status()

        self.assertEqual("Referred", actualResult)

        tProcedure = Procedure.objects.create(procedure_name="leeches")
        tProcedure.save()
        tProcedure2 = Procedure.objects.create(procedure_name="Bloodwork")
        tProcedure2.save()
        tProcedure3 = Procedure.objects.create(procedure_name="TAVR")
        tProcedure3.save()


        ap1 = AssignedProcedures.assign_procedure_to_patient(1,tPatient,tProcedure)
        ap2 = AssignedProcedures.assign_procedure_to_patient(2,tPatient,tProcedure2)
        ap3 = AssignedProcedures.assign_procedure_to_patient(3,tPatient,tProcedure3)

        expected_list = [tProcedure]
        final_procedures_list = tPatient.get_patient_next_procedures()
        self.assertListEqual(expected_list, final_procedures_list)

    def test_patient_today(self):
        from assigned_procedures.models import AssignedProcedures
        from procedures.models import Procedure

        tPatient = self.create_patient()
        tPatient.save()

        actualResult = tPatient.patient_status()

        self.assertEqual("Referred", actualResult)

        tProcedure = Procedure.objects.create(procedure_name="leeches")
        tProcedure.save()
        tProcedure2 = Procedure.objects.create(procedure_name="Bloodwork")
        tProcedure2.save()
        tProcedure3 = Procedure.objects.create(procedure_name="TAVR")
        tProcedure3.save()

        ap1 = AssignedProcedures.assign_procedure_to_patient(1, tPatient, tProcedure)
        self.assertFalse(tPatient.has_incomplete_procedure_today())
        ap1.scheduled = True
        ap1.save()
        ap2 = AssignedProcedures.assign_procedure_to_patient(2, tPatient, tProcedure2)
        ap3 = AssignedProcedures.assign_procedure_to_patient(3, tPatient, tProcedure3)

        expected_list = [tProcedure]
        final_procedures_list = tPatient.procedures_for_today()
        self.assertListEqual(expected_list, final_procedures_list)
        self.assertTrue(tPatient.has_incomplete_procedure_today())