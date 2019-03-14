from django.db import models
from procedures.models import Procedure


PHASE_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)


class Roadmap(models.Model):
    roadmap_name = models.CharField(max_length=100)

    def __str__(self):
        return self.roadmap_name


class RoadmapProcedureLink(models.Model):
    roadmap = models.ManyToManyField(Roadmap)
    procedure = models.ManyToManyField(Procedure)
    phase = models.CharField(max_length=5, choices=PHASE_CHOICES, default='')
