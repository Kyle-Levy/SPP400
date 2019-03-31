from django.test import TestCase
from patients import models
from patients.models import Patients
from assigned_procedures import models
from assigned_procedures.models import AssignedProcedures
from procedures import models
from procedures.models import Procedure
from datetime import date
from datetime import datetime

# Create your tests here.
class TestAssignedProcedures(TestCase):

    def create_assignedProcedure(self, first_name="Kyle", last_name="Dorce", bday=datetime(1996, 10, 24), referring_physician='Dr. Who', date_of_referral=datetime(2019, 1, 1)):
        tPatient = Patients.objects.create(first_name=first_name, last_name=last_name, bday=bday, referring_physician=referring_physician, date_of_referral=date_of_referral)
        tPatient.save()
        tProcedure = Procedure.objects.create(procedure_name="leeches")
        tAssignment = AssignedProcedures.assign_procedure_to_patient(1, tPatient, tProcedure)
        return tAssignment, tPatient, tProcedure

    def create_assignedProcedureReturnVisit(self):
        tPatient = Patients.objects.create(first_name="Kyle", last_name="Dorce", bday=datetime(1996, 10, 24))
        tProcedure = Procedure.objects.create(procedure_name="leeches")
        tAssignment = AssignedProcedures.assign_procedure_to_patient(1, tPatient, tProcedure, True)
        return tAssignment, tPatient, tProcedure

    def test_last_visit_id(self):
        testAssign, testPatient, testProcedure = self.create_assignedProcedure()
        self.assertEqual(AssignedProcedures.last_visit_id(testPatient), 1)

    def test_get_all_procedures(self):
        #one linked procedure case
        testAssign, testPatient, testProcedure = self.create_assignedProcedure()
        quiriedProcedure = AssignedProcedures.get_all_procedures(testPatient)
        self.assertEqual(quiriedProcedure[0],(1,testProcedure))
        #two linked procedures case
        tProcedure = Procedure.objects.create(procedure_name="bloodwork")
        AssignedProcedures.assign_procedure_to_patient(2,testPatient,tProcedure)
        quiriedProcedure = AssignedProcedures.get_all_procedures(testPatient)
        self.assertEqual(quiriedProcedure,[(1,testProcedure),(2,tProcedure)])

    def test_toggle_completed(self):
        testAssign, testPatient, testProcedure = self.create_assignedProcedure()
        result = AssignedProcedures.toggle_completed(searchPatient=testPatient,searchProcedure=testProcedure)
        self.assertTrue(result)
        result = AssignedProcedures.toggle_completed(searchPatient=testPatient,searchProcedure=testProcedure)
        self.assertFalse(result)

    def test_update_procedure_step(self):
        testAssign, testPatient, testProcedure = self.create_assignedProcedure()
        AssignedProcedures.update_procedure_step(2, testPatient,testProcedure)
        toCheck = AssignedProcedures.objects.get(patient=testPatient,procedure=testProcedure)
        self.assertEqual(toCheck.procedureStep,2)
