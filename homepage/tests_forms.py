from homepage.forms import LoginForm
from django.test import TestCase


class TestLoginForm(TestCase):

    def test_valid_form(self):
        form_data = {'username': 'testuser', 'password': 'mypass'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_password(self):
        form_data = {'username': 'testuser'}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_missing_username(self):
        form_data = {'password': 'mypass'}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_empty_fields(self):
        form_data = {}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
