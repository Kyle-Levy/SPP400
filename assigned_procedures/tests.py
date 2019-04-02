from django.test import TestCase
from patients import models
from patients.models import Patients
from assigned_procedures import models
from assigned_procedures.models import AssignedProcedures
from procedures import models
from procedures.models import Procedure
from roadmaps.models import Roadmap,RoadmapProcedureLink
from datetime import date
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from django.utils.timezone import now

# Tests labeled with "not actually a test" are helper functions
# labeled as "test" so they do not interfere with code coverage metrics
class TestAssignedProcedures(TestCase):

    def test_create_assignedProcedure(self, first_name="Kyle", last_name="Dorce", bday=datetime(1996, 10, 24), referring_physician='Dr. Who', date_of_referral=datetime(2019, 1, 1)):
        tPatient = Patients.objects.create(first_name=first_name, last_name=last_name, bday=bday, referring_physician=referring_physician, date_of_referral=date_of_referral)
        tPatient.save()
        tProcedure = Procedure.objects.create(procedure_name="leeches")
        tAssignment = AssignedProcedures.assign_procedure_to_patient(1, tPatient, tProcedure)
        return tAssignment, tPatient, tProcedure
    #Not actually a test
    def test_create_roadmap(self):
        tRoadmap = Roadmap.objects.create(roadmap_name="TAVR")
        tRoadmap.save()
        tProcedure = Procedure.objects.create(procedure_name="leaches")
        tProcedure.save()
        tProcedure2 = Procedure.objects.create(procedure_name="blood")
        tProcedure2.save()

        RoadmapProcedureLink.link_procedure_to_roadmap(tProcedure, tRoadmap, 1)

        RoadmapProcedureLink.link_procedure_to_roadmap(tProcedure2, tRoadmap, 2)

        return tRoadmap, tProcedure, tProcedure2

    def test_create_assignedProcedureReturnVisit(self):
        tPatient = Patients.objects.create(first_name="Kyle", last_name="Dorce", bday=datetime(1996, 10, 24))
        tProcedure = Procedure.objects.create(procedure_name="leeches")
        tAssignment = AssignedProcedures.assign_procedure_to_patient(1, tPatient, tProcedure, True)
        return tAssignment, tPatient, tProcedure


    def test_last_visit_id(self):
        testAssign, testPatient, testProcedure = self.test_create_assignedProcedure()
        self.assertEqual(AssignedProcedures.last_visit_id(testPatient), 1)

    def test_get_all_procedures(self):
        #one linked procedure case
        testAssign, testPatient, testProcedure = self.test_create_assignedProcedure()
        quiriedProcedure = AssignedProcedures.get_all_procedures(testPatient)
        self.assertEqual(quiriedProcedure[0],(testProcedure,1))
        #two linked procedures case
        tProcedure = Procedure.objects.create(procedure_name="bloodwork")
        AssignedProcedures.assign_procedure_to_patient(2,testPatient,tProcedure)
        quiriedProcedure = AssignedProcedures.get_all_procedures(testPatient)
        self.assertEqual(quiriedProcedure,[(testProcedure,1),(tProcedure,2)])

    def test_toggle_completed(self):
        testAssign, testPatient, testProcedure = self.test_create_assignedProcedure()
        result = AssignedProcedures.toggle_completed(searchPatient=testPatient,searchProcedure=testProcedure)
        self.assertTrue(result)
        result = AssignedProcedures.toggle_completed(searchPatient=testPatient,searchProcedure=testProcedure)
        self.assertFalse(result)

    def test_update_procedure_step(self):
        testAssign, testPatient, testProcedure = self.test_create_assignedProcedure()
        AssignedProcedures.update_procedure_step(2, testPatient,testProcedure)
        toCheck = AssignedProcedures.objects.get(patient=testPatient,procedure=testProcedure)
        self.assertEqual(toCheck.procedureStep,2)


    def test_convert_days_to_date(self):
        solution = timezone.now() + timedelta(days=3)
        self.assertEqual(AssignedProcedures.convert_days_to_date(3).year, solution.year)
        self.assertEqual(AssignedProcedures.convert_days_to_date(3).month, solution.month)
        self.assertEqual(AssignedProcedures.convert_days_to_date(3).day, solution.day)

    def test_check_goal_status(self):
        testAssign, testPatient, testProcedure = self.test_create_assignedProcedure()
        result = AssignedProcedures.check_goal_status(testPatient,testProcedure)
        self.assertEqual(result,"not scheduled")
        tAssignment = AssignedProcedures.assign_procedure_to_patient(step=1, patientToLink=testPatient, procedureToLink=testProcedure, proc_est=2, return_visit=True)
        resultz = AssignedProcedures.check_goal_status(testPatient,testProcedure,2)
        self.assertEqual(resultz, "in progress (on time)")
        AssignedProcedures.toggle_completed(testPatient,testProcedure,2)
        tAssignment = AssignedProcedures.assign_procedure_to_patient(step=1, patientToLink=testPatient, procedureToLink=testProcedure, proc_est=2, return_visit=True)
        resultz = AssignedProcedures.check_goal_status(testPatient,testProcedure,2)
        self.assertEqual(resultz, "completed (on time)")



    def test_add_roadmap_to_patient(self):
        tPatient = Patients.objects.create(first_name="Lyle", last_name="Magoo", bday=datetime(1996, 10, 24))
        tPatient.save()
        tRoadmap, tProcedure, tProcedure2 = self.test_create_roadmap()

        AssignedProcedures.add_roadmap_to_patient(tRoadmap, tPatient)
        toCheck = AssignedProcedures.get_all_procedures(tPatient)
        solution = [(tProcedure,1),(tProcedure2,2)]
        self.assertEqual(toCheck,solution)

    def test_remove_assigned_procedure(self):
        testAssign, testPatient, testProcedure = self.test_create_assignedProcedure()
        tProcedure = Procedure.objects.create(procedure_name="TAVR")
        AssignedProcedures.assign_procedure_to_patient(2, testPatient, tProcedure)
        AssignedProcedures.remove_assigned_procedure(testPatient, testProcedure, 1)
        toCheck = AssignedProcedures.get_all_procedures(testPatient)
        correct = [(tProcedure,2)]
        self.assertEqual(toCheck, correct)

    def test_update_all_patient_goal_flags(self):
        result = AssignedProcedures.update_all_patient_goal_flags()
        self.assertEqual(result, [])
        tPatient = Patients.objects.create(first_name="Kyle", last_name="Dorcey", bday=datetime(1996, 10, 24))
        tPatient.save()
        tPatient2 = Patients.objects.create(first_name="Mr", last_name="Magoo", bday=datetime(1996, 10, 24))
        tPatient2.save()

        testProcedure = Procedure.objects.create(procedure_name="Leaches")
        testProcedure.save()
        testProcedure2 = Procedure.objects.create(procedure_name="moo")
        testProcedure2.save()

        AssignedProcedures.assign_procedure_to_patient(1,tPatient,testProcedure)
        AssignedProcedures.assign_procedure_to_patient(2,tPatient,testProcedure2,-10)
        AssignedProcedures.assign_procedure_to_patient(1, tPatient2, testProcedure)
        AssignedProcedures.assign_procedure_to_patient(2, tPatient2, testProcedure2, -10)
        result = AssignedProcedures.update_all_patient_goal_flags()
        self.assertEqual(result,[tPatient, tPatient2])
