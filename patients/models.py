from django.db import models
from datetime import datetime
from datetime import timedelta
from django.utils import timezone

# Create your models here.


class Patients(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    bday = models.DateField(auto_now=False, auto_now_add=False)
    doc_notes = models.TextField()
    flagged = models.BooleanField(default=False)
    flagged_reason = models.TextField(default="")
    today_flag = models.BooleanField(default=False)
    today_flag_end = models.DateTimeField(default=datetime.now())
    today_flag_reason = models.TextField(default="")


    def toggle_today_flag(self):
        if self.today_flag is False:
            self.today_flag = True
            self.today_flag_end = timezone.now() + timedelta(days=1)
            return True
        else:
            self.today_flag = False
            self.today_flag_end(blank=True)
            return False

    #returns true if flag is still valid
    def check_today_flag(self):
        if self.today_flag is True and timezone.now() <= self.today_flag_end is True:
            return True
        if self.today_flag is True and timezone.now() > self.today_flag_end is True:
            self.toggle_today_flag()
            return False
        else:
            return False


