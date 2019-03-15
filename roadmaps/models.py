from django.db import models
from procedures.models import Procedure


class Roadmap(models.Model):
    roadmap_name = models.CharField(max_length=100)

    def __str__(self):
        return self.roadmap_name


class RoadmapProcedureLink(models.Model):
    roadmap = models.ManyToManyField(Roadmap)
    procedure = models.ManyToManyField(Procedure)
    #TODO phase should only allow values between 1 & some decided upper bound
    phase = models.IntegerField(default=1)

    @classmethod
    def link_procedure_to_roadmap(cls, procedure, roadmap, phase):
        new_link = RoadmapProcedureLink.objects.create(phase=phase)
        new_link.roadmap.add(roadmap)
        new_link.procedure.add(procedure)
        new_link.save()

        return new_link

    @staticmethod
    def get_procedures_from_roadmap(searchRoadmap):
        quiried_roadmap = RoadmapProcedureLink.objects.filter(roadmap=searchRoadmap.id)
        procedure_phase_list = []
        for procedures in quiried_roadmap:
            proc_name = procedures.procedure.__str__()
            proc_phase = procedures.phase
            procedure_phase_list.append((proc_name, proc_phase))
        return procedure_phase_list
