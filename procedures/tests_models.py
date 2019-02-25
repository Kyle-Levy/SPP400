from django.test import TestCase
from procedures import models
from procedures.models import Procedures



class TestProcedureModel(TestCase):

    def create_procedure(self, procedure_name="leeches"):
        return Procedures.objects.create(procedure_name=procedure_name)

    def test_str(self):
        test_procedure = self.create_procedure()

        self.assertEqual(str(test_procedure), "leeches")