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

    def create_assignedProcedure(self):
        tPatient = Patients.objects.create(first_name="Kyle", last_name="Dorce", bday=datetime(1996, 10, 24))
        tPatient.save()
        tProcedure = Procedure.objects.create(procedure_name="leeches")
        tAssignment = AssignedProcedures.assign_procedure_to_patient(1, tPatient, tProcedure)
        return tAssignment

    def create_assignedProcedureReturnVisit(self):
        tPatient = Patients.objects.create(first_name="Kyle", last_name="Dorce", bday=datetime(1996, 10, 24))
        tProcedure = Procedure.objects.create(procedure_name="leeches")
        tAssignment = AssignedProcedures(patient=tPatient, procedure=tProcedure, step=1, return_visit=True)

    def test_last_visit_id(self):
        testCase = self.create_assignedProcedure()
        self.assertEqual(AssignedProcedures.last_visit_id(testCase.patient), 2)