from django.db import models
from datetime import datetime
from datetime import timedelta
from django.utils import timezone


class Procedure(models.Model):
    procedure_name = models.CharField(max_length=1000, default="")
    procedure_info = models.CharField(max_length=1000, default="")
    # Flag for if a procedure has a previous step.
    procedure_flag = models.BooleanField
    # Roadmap foreign key will be made. Step number will be set inside Roadmap.


    def __str__(self):
        return self.procedure_name
