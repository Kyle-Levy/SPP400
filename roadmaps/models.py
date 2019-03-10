from django.db import models
from procedures.models import Procedure


PHASE_CHOICES = (
    '1',
    '2',
    '3',
    '4',
    '5',
)


class Roadmap(models.Model):
    roadmap_name = models.CharField(max_length=100)
    procedures = models.ManyToManyField(Procedure)
    phases = models.CharField(max_length=5, choices=PHASE_CHOICES)

    def __str__(self):
        return self.roadmap_name
