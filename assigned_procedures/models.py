from django.db import models
import procedures
import patients

# Create your models here.
class AssignedProcedures(models.Model):
    patients = models.ManyToManyField(patients)
    procedures = models.ManyToManyField(procedures)
    #procedure steps that share the same visitID and number are concurrent
    procedureStep = models.IntegerField()
    #visitID is a way to distinguish what step a patient is on
    #if they return for a different procedure (default is 1)
    visitID = models.IntegerField(default=1)
    completed = models.BooleanField(default=False)

    @classmethod
    def assign_procedure_to_patient(cls, patient, procedure, step, return_visit=False):
        if return_visit is True:
            new_visit_id = AssignedProcedures.last_visit_id(patient)
            new_assignment = cls(patients=patient, procedures=procedure, step=step, visitID=new_visit_id)
        else:
            new_assignment = cls(patients=patient, procedures=procedure,step=step)
        return new_assignment

    @staticmethod
    def last_visit_id(patient):
        return 1