from django.db import models
from datetime import datetime
from datetime import timedelta
from assigned_procedures.models import AssignedProcedures

# Create your models here.
class Analytics(models.Model):
    behind_procedure_perc = models.DecimalField(max_digits=5, decimal_places=2, default=000)

    @staticmethod
    def calculate_behind_procedure_prec():

        totalProc = 0
        for indivAssignedProc in AssignedProcedures.get_all_active_procedures():
            totalProc += 1

        behindProc = 0
        for flaggedPatients in AssignedProcedures.update_and_return_all_patient_goal_flags():
            if flaggedPatients.behind_flag is True:
                behindProc += 1

        percentBehind = (behindProc/totalProc) * 100

        Analytics.behind_procedure_perc = percentBehind

        return percentBehind

    @staticmethod
    def return_all_behind_procedures():
        allLateProcedures = []

        for incompleteProcedure in AssignedProcedures.get_all_active_procedures():
            incompleteProcedurePatient = incompleteProcedure.patient.all()[0]
            incompleteProcedureProc = incompleteProcedure.procedure.all()[0]


            assignedProcStatus = AssignedProcedures.check_goal_status(incompleteProcedurePatient, incompleteProcedureProc)
            if assignedProcStatus == "in progress (behind)":
                allLateProcedures.append(incompleteProcedure)

        return allLateProcedures

