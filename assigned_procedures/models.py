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

    #returns list of procedures associated with a patient/visitID
    @staticmethod
    def get_all_procedures(searchPatient, searchVisitID=1):
        quiriedAssignedProcedures = AssignedProcedures.objects.filter(patient=searchPatient.id, visitID=searchVisitID)
        procedureList = []
        for assignedProcedures in quiriedAssignedProcedures:
            quiriedProcedures = assignedProcedures.procedure.all()
            for procedures in quiriedProcedures:
                procedureList.append(procedures)

        return procedureList
