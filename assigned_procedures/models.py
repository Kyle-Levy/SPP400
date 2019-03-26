from patients import models
from patients.models import Patients
from procedures import models
from procedures.models import Procedure
from django.db import models

# Create your models here.
class AssignedProcedures(models.Model):
    patient = models.ManyToManyField(Patients)
    procedure = models.ManyToManyField(Procedure)
    #procedure steps that share the same visitID and number are concurrent
    procedureStep = models.IntegerField()
    #visitID is a way to distinguish what step a patient is on
    #if they return for a different procedure (default is 1)
    visitID = models.IntegerField(default=1)
    completed = models.BooleanField(default=False)

    @classmethod
    def assign_procedure_to_patient(cls, step, patientToLink,procedureToLink, return_visit=False):
        if return_visit is True:
            new_visit_id = AssignedProcedures.last_visit_id(patientToLink)
            new_assignment = cls(procedureStep=step, visitID=new_visit_id)
            new_assignment.patient.add(patientToLink)
            new_assignment.procedure.add(procedureToLink)
            new_assignment.save()
        else:
            new_assignment = AssignedProcedures.objects.create(procedureStep=step)
            new_assignment.patient.add(patientToLink)
            new_assignment.procedure.add(procedureToLink)
            new_assignment.save()

        return new_assignment

    #this method is used when a patient is returning for a new procedure
    @staticmethod
    def last_visit_id( plz):
        assignments =AssignedProcedures.objects.filter(patient=plz.id)
        maxVisitID = 0
        for retrieved in assignments:
            if retrieved.visitID > maxVisitID:
                maxVisitID = retrieved.visitID


        return maxVisitID

    #returns list of tuples structured: (step number, procedure object)
    @staticmethod
    def get_all_procedures(searchPatient, searchVisitID=1):
        quiriedAssignedProcedures = AssignedProcedures.objects.filter(patient=searchPatient.id, visitID=searchVisitID)
        procedureList = []
        for assignedProcedures in quiriedAssignedProcedures:
            procStep = assignedProcedures.procedureStep
            quiriedProcedures = assignedProcedures.procedure.all()
            for procedures in quiriedProcedures:
                procedureList.append( (procStep,procedures) )
        return procedureList


    @staticmethod
    def toggle_completed(searchPatient, searchProcedure, searchVisitID=1):
        quiriedAssignedProcedures = AssignedProcedures.objects.filter(patient=searchPatient.id, procedure=searchProcedure, visitID=searchVisitID)
        for assignedProc in quiriedAssignedProcedures:
            if assignedProc.completed is False:
                assignedProc.completed = True
                assignedProc.save()
                return True
            elif assignedProc.completed is True:
                assignedProc.completed = False
                assignedProc.save()
                return False

    @staticmethod
    def update_procedure_step(newStepNumber, searchPatient, searchProcedure, searchVisitID=1):
        quiriedAssignedProcedures = AssignedProcedures.objects.filter(patient=searchPatient.id, procedure=searchProcedure, visitID=searchVisitID)
        for assignedProc in quiriedAssignedProcedures:
            assignedProc.procedureStep = newStepNumber
            assignedProc.save()

