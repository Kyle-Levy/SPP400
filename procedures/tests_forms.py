from django.test import TestCase
from procedures.forms import ProceduresTemplate

class TestProcedureTemplate(TestCase):

    def test_name_expire_date_notes(self):
        form_data = {'procedure_name': 'bloodtest', 'expired_time': '11/20/19', 'procedure_date': '10/25/19',
                     'notes': 'Some notes'}
        form = ProceduresTemplate(data=form_data)
        self.assertTrue(form.is_valid())

    def test_name_expire_date(self):
        form_data = {'procedure_name': 'bloodtest', 'expired_time': '11/20/19', 'procedure_date': '10/25/19'}
        form = ProceduresTemplate(data=form_data)
        self.assertTrue(form.is_valid())

    def test_name_expire_notes(self):
        form_data = {'procedure_name': 'bloodtest', 'expired_time': '11/20/19', 'notes': 'Some notes'}
        form = ProceduresTemplate(data=form_data)
        self.assertTrue(form.is_valid())

    def test_name_date_notes(self):
        form_data = {'procedure_name': 'bloodtest', 'procedure_date': '10/25/19', 'notes': 'Some notes'}
        form = ProceduresTemplate(data=form_data)
        self.assertTrue(form.is_valid())

    def test_name_date(self):
        form_data = {'procedure_name': 'bloodtest', 'procedure_date': '10/25/19'}
        form = ProceduresTemplate(data=form_data)
        self.assertTrue(form.is_valid())

    def test_name_expire(self):
        form_data = {'procedure_name': 'bloodtest', 'expired_time': '11/20/19'}
        form = ProceduresTemplate(data=form_data)
        self.assertTrue(form.is_valid())

    def test_name_notes(self):
        form_data = {'procedure_name': 'bloodtest', 'notes': 'Some notes'}
        form = ProceduresTemplate(data=form_data)
        self.assertTrue(form.is_valid())

    def test_expire_date(self):
        form_data = {'expired_time': '11/20/19', 'procedure_date': '10/25/19'}
        form = ProceduresTemplate(data=form_data)
        self.assertFalse(form.is_valid())

    def test_expire_notes(self):
        form_data = {'expired_time': '11/20/19', 'notes': 'Some notes'}
        form = ProceduresTemplate(data=form_data)
        self.assertFalse(form.is_valid())

    def test_date_notes(self):
        form_data = {'procedure_date': '10/25/19', 'notes': 'Some notes'}
        form = ProceduresTemplate(data=form_data)
        self.assertFalse(form.is_valid())

    def test_name(self):
        form_data = {'procedure_name': 'bloodtest'}
        form = ProceduresTemplate(data=form_data)
        self.assertTrue(form.is_valid())

    def test_date(self):
        form_data = {'procedure_date': '10/25/19'}
        form = ProceduresTemplate(data=form_data)
        self.assertFalse(form.is_valid())

    def test_expire(self):
        form_data = {'expired_time': '11/20/19'}
        form = ProceduresTemplate(data=form_data)
        self.assertFalse(form.is_valid())

    def test_notes(self):
        form_data = {'notes': 'Some notes'}
        form = ProceduresTemplate(data=form_data)
        self.assertFalse(form.is_valid())
