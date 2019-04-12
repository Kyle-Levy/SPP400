from patients import models
from patients.models import Patients
from procedures import models
from procedures.models import Procedure
from roadmaps.models import Roadmap, RoadmapProcedureLink
from django.db import models
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from django.utils.timezone import now
import math




# Create your models here.
class AssignedProcedures(models.Model):
    patient = models.ManyToManyField(Patients)
    procedure = models.ManyToManyField(Procedure)
    # procedure steps that share the same visitID and number are concurrent
    procedureStep = models.IntegerField()
    # visitID is a way to distinguish what step a patient is on
    # if they return for a different procedure (default is 1)
    visitID = models.IntegerField(default=1)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(default=timezone.now)
    #ONLY check est_date_complete if the est_flag is TRUE
    est_date_complete = models.DateTimeField(default=timezone.now)
    #if est_flag is false the assigned procedure does not have a goal date and doesn't need to be checked
    est_flag = models.BooleanField(default=False)



    @classmethod
    def assign_procedure_to_patient(cls, step, patientToLink,procedureToLink, proc_est=0, return_visit=False):
        if proc_est is not 0 or procedureToLink.est_days_to_complete is not 0:
            est_flag = True
            if proc_est is not 0:
                proc_est = AssignedProcedures.convert_days_to_date(proc_est)
            else:
                proc_est = AssignedProcedures.convert_days_to_date(procedureToLink.est_days_to_complete)
        else:
            est_flag = False
            proc_est = timezone.now()

        if return_visit is True:
            new_visit_id = AssignedProcedures.last_visit_id(patientToLink) + 1
            new_assignment = AssignedProcedures.objects.create(procedureStep=step, visitID=new_visit_id, est_date_complete=proc_est, est_flag = est_flag)
            new_assignment.patient.add(patientToLink)
            new_assignment.procedure.add(procedureToLink)
            new_assignment.save()
        else:
            new_assignment = AssignedProcedures.objects.create(procedureStep=step, est_date_complete=proc_est, est_flag = est_flag)
            new_assignment.patient.add(patientToLink)
            new_assignment.procedure.add(procedureToLink)
            new_assignment.save()

        return new_assignment



    #returns a strings:
    #completed (on time)
    #completed (behind)
    #in progress (behind)
    #in progress (on time)
    #not scheduled
    #"in progress"/"completed" refers to whether the procedure has been completed or not
    #"behind"/"on time" refers to if the procedure is behind schedule or not.
    #KNOWN BUG: THIS DOES NOT WORK IF THE SAME PROCEDURE IS ASSIGNED AT DIFFERENT TIMES WITH DIFFERENT GOALS
    @staticmethod
    def check_goal_status(searchPatient, searchProcedure, searchVisitID=1):
        quiriedAssignedProcedures = AssignedProcedures.objects.filter(patient=searchPatient.id, procedure=searchProcedure, visitID=searchVisitID).select_related()
        for assignedProc in quiriedAssignedProcedures:

            if assignedProc.est_flag is True:

                if assignedProc.est_date_complete > timezone.now() and assignedProc.completed is False:
                    return "in progress (on time)"
                elif assignedProc.est_date_complete > timezone.now() and assignedProc.completed is True:
                    return "completed (on time)"
                elif assignedProc.est_date_complete < timezone.now() and assignedProc.completed is False:
                    return "in progress (behind)"
                elif assignedProc.est_date_complete < timezone.now() and assignedProc.completed is True:
                    return "completed (behind)"
            else:
                return "not scheduled"


    @staticmethod
    def convert_days_to_date(days):
        date = timezone.now() + timedelta(days=days)
        return date


    #this method is used when a patient is returning for a new procedure
    @staticmethod
    def last_visit_id(searchPatient):
        assignments = AssignedProcedures.objects.filter(patient=searchPatient.id)
        maxVisitID = 0
        for retrieved in assignments:
            if retrieved.visitID > maxVisitID:
                maxVisitID = retrieved.visitID

        return maxVisitID

    # returns a list of all procedures assigned to a patient
    # returned as a list of tuples structured: (procedure object, procedure step)
    @staticmethod
    def get_all_procedures(searchPatient, searchVisitID=1):
        quiriedAssignedProcedures = AssignedProcedures.objects.filter(patient=searchPatient.id, visitID=searchVisitID)
        procedureList = []
        for assignedProcedures in quiriedAssignedProcedures:
            procStep = assignedProcedures.procedureStep
            quiriedProcedures = assignedProcedures.procedure.all()
            for procedures in quiriedProcedures:
                procedureList.append((procedures, procStep))
        return procedureList

    @staticmethod
    def toggle_completed(searchPatient, searchProcedure, searchVisitID=1):
        quiriedAssignedProcedures = AssignedProcedures.objects.filter(patient=searchPatient.id,
                                                                      procedure=searchProcedure, visitID=searchVisitID)
        for assignedProc in quiriedAssignedProcedures:
            if assignedProc.completed is False:
                assignedProc.completed = True
                # assignedProc.date_completed = timezone.now
                assignedProc.save()
                return True
            elif assignedProc.completed is True:
                assignedProc.completed = False
                assignedProc.save()
                return False

    @staticmethod
    def update_procedure_step(newStepNumber, searchPatient, searchProcedure, searchVisitID=1):
        quiriedAssignedProcedures = AssignedProcedures.objects.filter(patient=searchPatient.id,
                                                                      procedure=searchProcedure, visitID=searchVisitID)
        for assignedProc in quiriedAssignedProcedures:
            assignedProc.procedureStep = newStepNumber
            assignedProc.save()

    @staticmethod
    def add_roadmap_to_patient(roadmap, patient, returnVisit=False):
        proceduresToAssign = RoadmapProcedureLink.get_procedures_from_roadmap(roadmap)
        for tempProc in proceduresToAssign:
            phaseNumber = tempProc[1] #aka step
            procedureObj = tempProc[0]
            proc_est = procedureObj.est_days_to_complete
            AssignedProcedures.assign_procedure_to_patient(phaseNumber,patient,procedureObj,proc_est, returnVisit)





    @staticmethod
    def remove_assigned_procedure(patientToChange, procedureToDelete, phase, visitID=1):
        quiriedAssignedProcedures = AssignedProcedures.objects.filter(patient=patientToChange.id,
                                                                      procedure=procedureToDelete, procedureStep=phase,
                                                                      visitID=visitID).delete()


    # updates all patient flags and returns a list of any flagged patients
    @staticmethod
    def update_and_return_all_patient_goal_flags():
        behindPatients = []
        quiriedAssignedProcedures = AssignedProcedures.objects.filter(completed=False)
        for assignedProc in quiriedAssignedProcedures:
            quiriedPatients = assignedProc.patient.all()
            for patient in quiriedPatients:
                behindCheck, behindProc = patient.flag_update()
                if behindCheck or patient.flagged is True:
                    behindPatients.append(patient)
        return list(set(behindPatients))


    @staticmethod
    def get_all_active_procedures():
        allAssignedProcedures = []
        quiriedAssignedProcedures = AssignedProcedures.objects.filter(completed=False)
        for assignedProc in quiriedAssignedProcedures:
            allAssignedProcedures.append(assignedProc)
        return allAssignedProcedures

    @staticmethod
    def get_all_complete_procedures():
        allAssignedProcedures = []
        quiriedAssignedProcedures = AssignedProcedures.objects.filter(completed=True)
        for assignedProc in quiriedAssignedProcedures:
            allAssignedProcedures.append(assignedProc)
        return allAssignedProcedures

    @staticmethod
    def average_completion_time(procedure_id):
        completed_procedures = AssignedProcedures.objects.filter(completed=True, procedure__id=procedure_id)
        total_days = 0
        total_procedures = 0
        for procedure in completed_procedures:
            total_days += (procedure.date_completed - procedure.created_at).days
            total_procedures += 1

        if total_days == 0:
            return "0"
        return str(int(math.floor(abs(total_days/total_procedures))))

