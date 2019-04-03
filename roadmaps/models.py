from django.db import models
from procedures.models import Procedure


class Roadmap(models.Model):
    roadmap_name = models.CharField(max_length=100)
    est_days_to_complete = models.IntegerField(default=0)


    def __str__(self):
        return self.roadmap_name

    # timeFrame = days, weeks, months
    # number = number of days/weeks/months
    def add_time_estimate(self, numberOf, timeFrame):
        if timeFrame == "days":
            self.est_days_to_complete = numberOf
            self.save()
            return True
        elif timeFrame == "weeks":
            self.est_days_to_complete = int(numberOf) * 7
            self.save()
            return True

        else:
            return False

    @staticmethod
    def update_roadmap_name(new_roadmap_name, current_roadmap):
        quiried_roadmap = Roadmap.objects.filter(id=current_roadmap.id)
        for roadmap in quiried_roadmap:
            roadmap.roadmap_name = new_roadmap_name




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
            proc_phase = procedures.phase
            proc_query = procedures.procedure.all()
            for proc_name in proc_query:
                procedure_phase_list.append((proc_name, proc_phase))
        return procedure_phase_list

    @staticmethod
    def update_phase_for_procedure(current_roadmap, current_procedure, new_phase_number):
        quiried_procedures = RoadmapProcedureLink.objects.filter(roadmap=current_roadmap.id, procedure=current_procedure.id)
        for procedure in quiried_procedures:
            procedure.phase = new_phase_number

    @staticmethod
    def remove_pair_from_roadmap(roadmap_id,procedure_id, phase_number ):
        queried_pairs = RoadmapProcedureLink.objects.filter(roadmap=roadmap_id, procedure=procedure_id, phase=phase_number)
        for item in queried_pairs:
            item.delete()

    @staticmethod
    def remove_all_pairs_from_roadmap(roadmap_id):
        queried_pairs = RoadmapProcedureLink.objects.filter(roadmap=roadmap_id)
        for item in queried_pairs:
            item.delete()

    @staticmethod
    def seperate_by_phase(roadmap_pairs):
        seperated_by_phase = {}

        for procedure, phase in roadmap_pairs:
            if phase in seperated_by_phase:
                seperated_by_phase[phase].append(procedure)
            else:
                seperated_by_phase[phase] = [procedure]

        return seperated_by_phase