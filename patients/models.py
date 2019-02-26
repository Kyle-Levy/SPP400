from django.db import models
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from django.utils.timezone import now
# Create your models here.


class Patients(models.Model):
    first_name = models.CharField(max_length=150, default="")
    last_name = models.CharField(max_length=150, default="")
    bday = models.DateField(auto_now=False, auto_now_add=False)
    doc_notes = models.CharField(max_length = 1000, default="")
    flagged = models.BooleanField(default=False)
    patient_flagged_reason = models.CharField(max_length = 1000, default="")
    today_flag = models.BooleanField(default=False)
    today_flag_end = models.DateTimeField(default=timezone.now)
    today_flag_reason = models.CharField(max_length = 1000, default="")


    @classmethod
    def create_patient(cls, first_name, last_name, birth_date):
        patient = cls(first_name=first_name, last_name=last_name, bday=birth_date)
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

    #returns true if flag is still valid
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




