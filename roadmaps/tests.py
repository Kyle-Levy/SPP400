from django.test import TestCase
from procedures.models import Procedure
from roadmaps.models import Roadmap,RoadmapProcedureLink


class TestRoadmaps(TestCase):

    def create_RoadmapProcedureLink(self, roadmap_name='TAVR', procedure_name='blood work', procedure_info='extract blood', phases=1):
        tRoadmap = Roadmap.objects.create(roadmap_name=roadmap_name)
        tRoadmap.save()
        tProcedure = Procedure.objects.create(procedure_name=procedure_name)
        tProcedure.save()

        tRoadmapProcedureLink = RoadmapProcedureLink.link_procedure_to_roadmap(tProcedure,tRoadmap,1)

        return tRoadmap, tProcedure, tRoadmapProcedureLink

    def test_get_procedures_from_roadmap(self):
        testRoadmap, testProc, testRoadmap = self.create_RoadmapProcedureLink()

        test = RoadmapProcedureLink.get_procedures_from_roadmap(testRoadmap)
        want = [(testProc,1)]
        self.assertEqual(test, want)