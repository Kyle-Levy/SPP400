from django.db import models
from datetime import datetime
from datetime import timedelta
from django.utils import timezone


class Procedure(models.Model):
    procedure_name = models.CharField(max_length=1000, default="")
    procedure_info = models.CharField(max_length=1000, default="")
    est_days_to_complete = models.IntegerField(default=0)



    def __str__(self):
        return self.procedure_name

    # timeFrame = days, weeks, months
    # number = number of days/weeks/months
    def add_time_estimate(self, numberOf, timeFrame):
        if timeFrame is "days":
            self.est_days_to_complete = numberOf
            self.save()
            return True
        elif timeFrame is "weeks":
            self.est_days_to_complete = numberOf * 7
            self.save()
            return True

        else:
            return False
