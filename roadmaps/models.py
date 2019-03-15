from django.db import models
from procedures.models import Procedure


class Roadmap(models.Model):
    roadmap_name = models.CharField(max_length=100)

    def __str__(self):
        return self.roadmap_name


class RoadmapProcedureLink(models.Model):
    roadmap = models.ManyToManyField(Roadmap)
    procedure = models.ManyToManyField(Procedure)
    phase = models.IntegerField(default=1)

    @classmethod
    def link_procedure_to_roadmap(cls, procedure, roadmap, phase):
        new_link = RoadmapProcedureLink.objects.create(phase=phase)
        new_link.roadmap.add(roadmap)
        new_link.procedure.add(procedure)
        new_link.save()

        return new_link
