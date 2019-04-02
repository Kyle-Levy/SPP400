from patients.forms import *
from django.test import TestCase


class TestPatientForm(TestCase):

    def test_valid_form(self):
        form_data = {'first_name': 'John', 'last_name': 'Smith', 'record_number': 'a', 'birth_date': '01/01/1950',
                     'referring_physician': 'Dr. Who', 'date_of_referral': '2019-01-01'}
        form = NewPatient(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_date(self):
        form_data = {'first_name': 'John', 'last_name': 'Smith', 'record_number': 'a', 'birth_date': '418',
                     'referring_physician': 'Dr. Who', 'date_of_referral': '2019-01-01'}
        form = NewPatient(data=form_data)
        self.assertFalse(form.is_valid())

    def test_missing_date(self):
        form_data = {'first_name': 'John', 'last_name': 'Smith', 'record_number': 'a', 'referring_physician': 'Dr. Who',
                     'date_of_referral': '2019-01-01'}
        form = NewPatient(data=form_data)
        self.assertFalse(form.is_valid())

    def test_missing_first_name(self):
        form_data = {'last_name': 'Smith', 'birth_date': '418', 'record_number': 'a', 'referring_physician': 'Dr. Who',
                     'date_of_referral': '2019-01-01'}
        form = NewPatient(data=form_data)
        self.assertFalse(form.is_valid())

    def test_missing_last_name(self):
        form_data = {'first_name': 'John', 'birth_date': '418', 'record_number': 'a', 'referring_physician': 'Dr. Who',
                     'date_of_referral': '2019-01-01'}
        form = NewPatient(data=form_data)
        self.assertFalse(form.is_valid())

    def test_empty_fields(self):
        form_data = {}
        form = NewPatient(data=form_data)
        self.assertFalse(form.is_valid())


class TestFlagForm(TestCase):

    def test_valid_form(self):
        form_data = {'notes': "Didn't respond to emails."}
        form = FlagForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_field(self):
        form_data = {}
        form = FlagForm(data=form_data)
        self.assertFalse(form.is_valid())
