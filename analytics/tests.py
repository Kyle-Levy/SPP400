from django.test import TestCase
from datetime import datetime
from datetime import timedelta
from analytics.models import Analytics
from assigned_procedures.models import AssignedProcedures
from procedures.models import Procedure
from patients.models import Patients
from django.utils import timezone


# Create your tests here.
class analytics_tests(TestCase):

    def test_create_test_inputs(self):
        tpatient = Patients.objects.create(first_name="test", last_name="testlast", bday=datetime(2010, 2, 3))
        tprocedure = Procedure.objects.create(procedure_name="TAVR", est_days_to_complete=12)
        tassignedProc = AssignedProcedures.assign_procedure_to_patient(1, tpatient, tprocedure)

        return tpatient, tprocedure, tassignedProc

    def test_calculate_behind_procedure_prec(self):
        tpatient, tprocedure, tassignedProc = self.test_create_test_inputs()

        self.assertEqual(Analytics.calculate_behind_procedure_prec(), 0)

        tprocedure2 = Procedure.objects.create(procedure_name="TAVR Old", est_days_to_complete=-2)

        AssignedProcedures.assign_procedure_to_patient(2, tpatient, tprocedure2)

        self.assertEqual(Analytics.calculate_behind_procedure_prec(), 50)
        self.assertEqual(Analytics.behind_procedure_perc, 50)

    def test_return_all_behind_procedures(self):
        tpatient, tprocedure, tassignedProc = self.test_create_test_inputs()
        self.assertEqual(Analytics.return_all_behind_procedures(), [])

        tprocedure2 = Procedure.objects.create(procedure_name="TAVR Old", est_days_to_complete=-2)

        solution = AssignedProcedures.assign_procedure_to_patient(2, tpatient, tprocedure2)

        self.assertEqual(Analytics.return_all_behind_procedures(), [solution])

    def test_get_all_done_patients_within_6_months(self):
        tpatient, tprocedure, tassignedProc = self.test_create_test_inputs()
        self.assertListEqual(Analytics.get_all_done_patients_within_6_months(), [])

        tassignedProc.completed = True
        tassignedProc.save()

        self.assertListEqual(Analytics.get_all_done_patients_within_6_months(), [tpatient])

    def test_get_all_done_patients_within_6_months_data(self):
        tpatient, tprocedure, tassignedProc = self.test_create_test_inputs()
        expected_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertListEqual(Analytics.get_all_done_patients_within_6_months_data(), expected_data)

        current_month = timezone.now().date().month

        tassignedProc.completed = True
        tassignedProc.save()

        expected_data[current_month - 1] = 1
        self.assertListEqual(Analytics.get_all_done_patients_within_6_months_data(), expected_data)
