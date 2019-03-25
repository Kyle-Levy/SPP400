from django.test import TestCase
from procedures.models import Procedure
from roadmaps.models import Roadmap,RoadmapProcedureLink


class TestRoadmaps(TestCase):

    def create_Roadmap(self, roadmap_name='TAVR2'):
        tRoadmap = Roadmap.objects.create(roadmap_name=roadmap_name)
        tRoadmap.save()

        return tRoadmap

    def test_update_roadmap_name(self, initial_name='TAVR', new_name='TAVR2'):
        tRoadmap = Roadmap.objects.create(roadmap_name=initial_name)
        tRoadmap.save()

        roadmap_id = tRoadmap.id

        tRoadmap.update_roadmap_name(new_name, roadmap_id)

        self.assertEqual(tRoadmap.roadmap_name, new_name)

    def create_RoadmapProcedureLink(self, roadmap_name='TAVR', procedure_name='blood work', procedure_info='extract blood', phases=1):
        tRoadmap = Roadmap.objects.create(roadmap_name=roadmap_name)
        tRoadmap.save()
        tProcedure = Procedure.objects.create(procedure_name=procedure_name)
        tProcedure.save()

        tRoadmapProcedureLink = RoadmapProcedureLink.link_procedure_to_roadmap(tProcedure, tRoadmap, 1)

        return tRoadmap, tProcedure, tRoadmapProcedureLink

    def test_get_procedures_from_roadmap(self, roadmap_name='TAVR', procedure_name1='blood work', procedure_name2='urine test'):
        t_roadmap = Roadmap.objects.create(roadmap_name=roadmap_name)
        t_roadmap.save()
        t_procedure1 = Procedure.objects.create(procedure_name=procedure_name1)
        t_procedure1.save()
        t_procedure2 = Procedure.objects.create(procedure_name=procedure_name2)
        t_procedure2.save()

        RoadmapProcedureLink.link_procedure_to_roadmap(t_procedure1, t_roadmap, 1)
        RoadmapProcedureLink.link_procedure_to_roadmap(t_procedure2, t_roadmap, 2)

        roadmap_list = RoadmapProcedureLink.get_procedures_from_roadmap(t_roadmap)

        self.assertEqual(roadmap_list, [('blood work', 1), ('urine test', 2)])
