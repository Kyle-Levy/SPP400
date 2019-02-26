from django.db import models
from datetime import datetime
from datetime import timedelta
from django.utils import timezone


class Procedures(models.Model):
    procedure_name = models.CharField(max_length=1000, default="")
    procedure_info = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.procedure_name
