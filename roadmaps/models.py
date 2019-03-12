from django.db import models
from procedures.models import Procedure


PHASE_CHOICES = (
    ('ONE', '1'),
    ('TWO', '2'),
    ('THREE', '3'),
    ('FOUR', '4'),
    ('FIVE', '5'),
)


class Roadmap(models.Model):
    roadmap_name = models.CharField(max_length=100)
    procedures = models.ManyToManyField(Procedure)
    phases = models.CharField(max_length=5, choices=PHASE_CHOICES)

    def __str__(self):
        return self.roadmap_name
