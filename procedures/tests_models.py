from django.test import TestCase
from procedures import models
from procedures.models import Procedure



class TestProcedureModel(TestCase):

    def test_create_procedure(self, procedure_name="leeches"):
        tproc = Procedure.objects.create(procedure_name=procedure_name)
        tproc.save()
        return tproc

    def test_str(self):
        test_procedure = self.test_create_procedure()

        self.assertEqual(str(test_procedure), "leeches")

    def test_add_time_estimate(self):
        tproc = self.test_create_procedure()
        tproc.add_time_estimate(2, "days")
        self.assertEqual(tproc.est_days_to_complete, 2)
        tproc.add_time_estimate(3, "weeks")
        self.assertEqual(tproc.est_days_to_complete, 21)
