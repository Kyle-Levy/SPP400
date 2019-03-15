from django.test import TestCase
from roadmaps.models import Roadmap,Procedure,RoadmapProcedureLink


class TestRoadmaps(TestCase):

    def create_RoadmapProcedureLink(self, roadmap_name='TAVR', procedure_name='blood work', procedure_info='extract blood', phases=('ONE', '1')):
        tRoadmap = Roadmap.objects.create(roadmap_name=roadmap_name)
        tProcedure = Procedure.objects.create(procedure_name=procedure_name, procedure_info=procedure_info)
        # replace this with a function for link creation.
        tRoadmapProcedureLink = RoadmapProcedureLink.objects.create(phases=phases)
        return tRoadmap, tProcedure, tRoadmapProcedureLink
