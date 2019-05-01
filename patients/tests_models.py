from django.test import TestCase
from patients.models import Patients
from assigned_procedures.models import AssignedProcedures
from procedures.models import Procedure
from datetime import datetime


class TestPatientsModel(TestCase):

    def create_patient(self, first_name='Steve', last_name='Stevens', bday='2000-01-01', referring_physician='Dr. Who',
                       date_of_referral='2019-01-01'):
        return Patients.objects.create(first_name=first_name, last_name=last_name, bday=bday,
                                       referring_physician=referring_physician, date_of_referral=date_of_referral)

    def test_str(self):
        test_patient = self.create_patient()

        self.assertEqual(str(test_patient), 'Steve Stevens')

    def test_has_missed_appointment(self):
        tPatient = Patients.objects.create(first_name="Kyle", last_name="Moo", bday="2000-01-01", referring_physician="Mr magoo",
                                date_of_referral="2019-12-22")
        tProcedure = Procedure.objects.create(procedure_name="leaches")
        tProcedure2 = Procedure.objects.create(procedure_name="bloodwork")

        tAssignedProc = AssignedProcedures.assign_procedure_to_patient(1,tPatient,tProcedure)
        tAssignedProc.date_scheduled = datetime(2019,3,22)
        tAssignedProc.scheduled = True
        AssignedProcedures.toggle_completed(tPatient,tProcedure)

        tAssignedProc2 = AssignedProcedures.assign_procedure_to_patient(2,tPatient,tProcedure2)
        tAssignedProc2.date_scheduled = datetime(2019,2,22)
        tAssignedProc2.scheduled = True
        AssignedProcedures.toggle_completed(tPatient,tProcedure2)
        tAssignedProc.save()
        tAssignedProc2.save()

        self.assertEqual(True,tPatient.has_missed_appointment())