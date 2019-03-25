from django.test import RequestFactory, TestCase
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User
from procedures.views import index, new_procedure, view_procedure, update_procedure, delete_this_procedure
from roadmaps.views import roadmaps_index, create_roadmap
from .models import Procedure, Roadmap, RoadmapProcedureLink


class TestProcedures(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware()
        self.user = User.objects.create_superuser('testuser', 'testuser@email.com', 'supersecretpass')
        self.user.save()

        # Creating procedures for testing the ability to add them to a roadmap
        request = self.factory.post('create/', {'procedure_name': 'Object One', 'notes': 'These are test notes'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        new_procedure(request)
        self.test_object_one = Procedure.objects.get(procedure_name='Object One',
                                                     procedure_info='These are test notes')

        # Creating procedures for testing the ability to add them to a roadmap
        request = self.factory.post('create/', {'procedure_name': 'Object Two', 'notes': 'These are test notes'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        new_procedure(request)
        self.test_object_two = Procedure.objects.get(procedure_name='Object Two',
                                                     procedure_info='These are test notes')

        # Creating procedures for testing the ability to add them to a roadmap
        request = self.factory.post('create/', {'procedure_name': 'Object Three', 'notes': 'These are test notes'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        new_procedure(request)
        self.test_object_three = Procedure.objects.get(procedure_name='Object Three',
                                                       procedure_info='These are test notes')

    def test_get_roadmaps(self):
        request = self.factory.get('/roadmaps/')
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = roadmaps_index(request)
        self.assertEqual(response.status_code, 200)

    def test_post_roadmaps(self):
        request = self.factory.post('/roadmaps/')
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = roadmaps_index(request)
        self.assertEqual(response.status_code, 302)

    def test_get_create_roadmap(self):
        request = self.factory.get('/roadmaps/create/')
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = create_roadmap(request)
        self.assertEqual(response.status_code, 200)

    def test_create_roadmap_valid(self):
        request = self.factory.post('/roadmaps/create/', {'roadmap_name': 'Test Roadmap'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = create_roadmap(request)
        self.assertEqual(response.status_code, 302)

        test_roadmap = Roadmap.objects.get(roadmap_name='Test Roadmap')
        self.assertIsNotNone(test_roadmap)

    def test_create_roadmap_invalid(self):
        request = self.factory.post('/roadmaps/create/', { })
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = create_roadmap(request)
        self.assertEqual(response.status_code, 401)

        