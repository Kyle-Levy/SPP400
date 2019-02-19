from django.db import models

# Create your models here.


class Patients(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    bday = models.DateField(auto_now=False, auto_now_add=False)
    doc_notes = models.TextField()
    flagged = models.BooleanField(default=False)
    today_flag = models.BooleanField(default=False)
