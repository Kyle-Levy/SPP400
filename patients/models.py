from django.db import models
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from django.utils.timezone import now


# Create your models here.


class Patients(models.Model):
    patient_id = models.IntegerField(default=00000)
    first_name = models.CharField(max_length=150, default="")
    last_name = models.CharField(max_length=150, default="")
    bday = models.DateField(auto_now=False, auto_now_add=False)
    doc_notes = models.CharField(max_length=1000, default="")
    flagged = models.BooleanField(default=False)
    patient_flagged_reason = models.CharField(max_length=1000, default="")
    today_flag = models.BooleanField(default=False)
    today_flag_end = models.DateTimeField(default=timezone.now)
    today_flag_reason = models.CharField(max_length=1000, default="")
    record_number = models.CharField(max_length=150, default="########")

    # Foreign key for a patent's procedure step.
    # PROCEDURE_STEP = PHASE NUMBER. I'M TOO SCARED TO
    # REFACTOR IT RIGHT NOW
    procedure_step = models.CharField(max_length=1000, default="")
    # Fields for referring physician and date of referral.
    referring_physician = models.CharField(max_length=150, default='')
    date_of_referral = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now)
    # flag used to show when a patient is behind for a procedure
    behind_flag = models.BooleanField(default=False)

    @classmethod
    def create_patient(cls, first_name, last_name, birth_date, record_number, referring_physician, date_of_referral):
        patient = cls(first_name=first_name, last_name=last_name, bday=birth_date, record_number=record_number,
                      referring_physician=referring_physician, date_of_referral=date_of_referral)
        return patient

    def toggle_today_flag(self):
        if self.today_flag is False:
            self.today_flag = True
            self.today_flag_end = timezone.now() + timedelta(days=1)
            return True
        else:
            self.today_flag = False
            self.today_flag_end = None
            return False

    # returns true if flag is still valid
    def check_today_flag(self):
        if self.today_flag is True and timezone.now().day <= self.today_flag_end.day is True:
            return True
        elif self.today_flag is True and timezone.now().day > self.today_flag_end.day is True:
            self.toggle_today_flag()
            return False
        else:
            return False

    def toggle_flag(self):
        if self.flagged is True:
            self.flagged = False
            return False
        elif self.flagged is False:
            self.flagged = True
            return True

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_absolute_url(self):
        # This returns the url for a patients profile when called on a patient
        return 'patients/profile/?id=' % self.id

    def save(self, *args, **kwargs):
        self.search_field = str(self.first_name) + str(self.last_name) + str(self.record_number)
        super(Patients, self).save(*args, **kwargs)

    # Updates the "behind_flag" to "true" if there are any
    # assigned procedures that are in progress and behind schedule.
    # it then returns a tuple structured (True, Problematic Procedure)
    # and if none are behind returns False

    def flag_update(self):
        import assigned_procedures
        from assigned_procedures.models import AssignedProcedures

        assignedProcs = AssignedProcedures.get_all_procedures(self)
        for procedureToCheck in assignedProcs:
            result = AssignedProcedures.check_goal_status(self, procedureToCheck[0], 1)
            if result == "in progress (behind)":
                self.behind_flag = True
                self.save()
                return procedureToCheck[0], True

        self.behind_flag = False
        self.save()
        return None, False

    def patient_is_done(self):
        from assigned_procedures.models import AssignedProcedures
        if (not AssignedProcedures.get_all_active_procedures_for_patient(self)) and (
                AssignedProcedures.get_all_procedures_completed_by_patient(self)):
            # This patient has been assigned procedures and has completed them all
            return True
        else:
            return False

    def patient_completion_date(self):
        from assigned_procedures.models import AssignedProcedures
        return AssignedProcedures.get_last_completed_date(self)

    def patient_status(self):
        from assigned_procedures.models import AssignedProcedures
        # If the patient doesn't have any procedures assigned, then they've only been referred
        # If the patient has procedures, but the first_incomplete_phase is not the final phase, then they aren't ready for the final procedure(s)
        # Only procedures left for the patient are the final ones
        # Patient has procedures that are all completed
        first_incomplete_phase = AssignedProcedures.get_first_incomplete_phase(self)
        final_phase_for_patient = AssignedProcedures.get_final_phase_number(self)
        if not AssignedProcedures.objects.filter(patient=self):
            return "Referred"
        elif first_incomplete_phase < final_phase_for_patient:
            return "In-Progress"
        elif first_incomplete_phase == final_phase_for_patient:
            return "Ready"
        else:
            return "Done"

    def patient_final_procedures(self):
        from assigned_procedures.models import AssignedProcedures
        final_phase_for_patient = AssignedProcedures.get_final_phase_number(self)
        final_procedure_list = []

        final_procedures = AssignedProcedures.objects.filter(patient=self, phaseNumber=final_phase_for_patient)
        for single_procedure in final_procedures:
            final_procedure_list.append(single_procedure.procedure.all()[0])

        return final_procedure_list

    def get_patient_next_procedures(self):
        from assigned_procedures.models import AssignedProcedures
        first_incomplete_phase = AssignedProcedures.get_first_incomplete_phase(self)
        next_procedure_list = []

        final_procedures = AssignedProcedures.objects.filter(patient=self, phaseNumber=first_incomplete_phase,
                                                             completed=False)

        for incomplete_procedure in final_procedures:
            next_procedure_list.append(incomplete_procedure.procedure.all()[0])

        return next_procedure_list

    def has_incomplete_procedure_today(self):
        from assigned_procedures.models import AssignedProcedures
        today = timezone.now()

        todays_incomplete_procedures = AssignedProcedures.objects.filter(patient=self, completed=False,
                                                                         date_scheduled__year=today.year,
                                                                         date_scheduled__month=today.month,
                                                                         date_scheduled__day=today.day,
                                                                         scheduled=True)
        if todays_incomplete_procedures:
            return True
        else:
            return False

    def procedures_for_today(self):
        from assigned_procedures.models import AssignedProcedures
        today = timezone.now()
        procedure_list = []
        todays_incomplete_procedures = AssignedProcedures.objects.filter(patient=self, completed=False,
                                                                         date_scheduled__year=today.year,
                                                                         date_scheduled__month=today.month,
                                                                         date_scheduled__day=today.day,
                                                                         scheduled=True)

        for assigned_proc_item in todays_incomplete_procedures:
            procedure_list.append(assigned_proc_item.procedure.all()[0])

        return procedure_list

    def has_missed_appointment(self):
        from assigned_procedures.models import AssignedProcedures

        today = timezone.now()
        procedure_list = ""
        todays_incomplete_procedures = AssignedProcedures.objects.filter(patient=self, completed=False, scheduled=True)

        for assigned_proc in todays_incomplete_procedures:
            if assigned_proc.date_scheduled.date() < today.date():
                procedure_list += assigned_proc.procedure.all()[0].procedure_name + ', '

        # This line removes the last comma and space
        procedure_list = procedure_list[:-2]

        if procedure_list != "":
            self.today_flag_reason = "Missed appointment(s): " + procedure_list
            self.save()
            return True
        else:
            self.today_flag_reason = procedure_list
            self.save()
            return False
