from patients.forms import NewPatient
from django.test import TestCase


class TestPatientForm(TestCase):

    def test_valid_form(self):
        form_data = {'first_name': 'John', 'last_name': 'Smith', 'birth_date': '01/01/1950'}
        form = NewPatient(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_date(self):
        form_data = {'first_name': 'John', 'last_name': 'Smith', 'birth_date': '418'}
        form = NewPatient(data=form_data)
        self.assertFalse(form.is_valid())

    def test_missing_date(self):
        form_data = {'first_name': 'John', 'last_name': 'Smith'}
        form = NewPatient(data=form_data)
        self.assertFalse(form.is_valid())

    def test_missing_first_name(self):
        form_data = {'last_name': 'Smith', 'birth_date': '418'}
        form = NewPatient(data=form_data)
        self.assertFalse(form.is_valid())

    def test_missing_last_name(self):
        form_data = {'first_name': 'John', 'birth_date': '418'}
        form = NewPatient(data=form_data)
        self.assertFalse(form.is_valid())

    def test_empty_fields(self):
        form_data = {}
        form = NewPatient(data=form_data)
        self.assertFalse(form.is_valid())
