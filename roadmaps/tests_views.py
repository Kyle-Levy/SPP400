from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User
from procedures.views import new_procedure
from roadmaps.views import *
from .models import Procedure, Roadmap, RoadmapProcedureLink


class TestProcedures(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware()
        self.user = User.objects.create_superuser('testuser', 'testuser@email.com', 'supersecretpass')
        self.user.save()

        # Creating procedures for testing the ability to add them to a roadmap
        request = self.factory.post('create/', {'procedure_name': 'Object One', 'notes': 'These are test notes',
                                                'time_frame': 'days', 'time': '22'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        new_procedure(request)
        self.test_object_one = Procedure.objects.get(procedure_name='Object One',
                                                     procedure_info='These are test notes')

        # Creating procedures for testing the ability to add them to a roadmap
        request = self.factory.post('create/', {'procedure_name': 'Object Two', 'notes': 'These are test notes',
                                                'time_frame': 'days', 'time': '22'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        new_procedure(request)
        self.test_object_two = Procedure.objects.get(procedure_name='Object Two',
                                                     procedure_info='These are test notes')

        # Creating procedures for testing the ability to add them to a roadmap
        request = self.factory.post('create/', {'procedure_name': 'Object Three', 'notes': 'These are test notes',
                                                'time_frame': 'days', 'time': '22'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        new_procedure(request)
        self.test_object_three = Procedure.objects.get(procedure_name='Object Three',
                                                       procedure_info='These are test notes')

        request = self.factory.post('/roadmaps/create/',
                                    {'roadmap_name': 'Test Roadmap', 'time_frame': 'days', 'time': '22'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        create_roadmap(request)
        self.test_roadmap = Roadmap.objects.get(roadmap_name='Test Roadmap')

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
        request = self.factory.post('/roadmaps/create/',
                                    {'roadmap_name': 'Created Roadmap', 'time_frame': 'days', 'time': '22'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = create_roadmap(request)
        self.assertEqual(response.status_code, 302)

        test_roadmap = Roadmap.objects.get(roadmap_name='Created Roadmap')
        self.assertIsNotNone(test_roadmap)

    def test_create_roadmap_invalid(self):
        request = self.factory.post('/roadmaps/create/', {})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = create_roadmap(request)
        self.assertEqual(response.status_code, 302)

    def test_get_view_roadmap_valid(self):
        request = self.factory.get('/roadmaps/view_roadmap/?id=' + str(self.test_roadmap.id))
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = view_roadmap(request)

        self.assertEqual(response.status_code, 200)

    def test_get_view_roadmap_invalid(self):
        request = self.factory.get('/roadmaps/view_roadmap/?id=' + str(self.test_roadmap.id + 99999))
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = view_roadmap(request)

        self.assertEqual(response.status_code, 302)

    def test_get_modify_roadmap_valid(self):
        request = self.factory.get('/roadmaps/view_roadmap/modify_roadmap/?id=' + str(self.test_roadmap.id))
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = modify_roadmap(request)

        self.assertEqual(response.status_code, 200)

    def test_get_modify_roadmap_invalid(self):
        request = self.factory.get('/roadmaps/view_roadmap/modify_roadmap/?id=' + str(self.test_roadmap.id + 99999))
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = modify_roadmap(request)

        self.assertEqual(response.status_code, 302)

    def test_add_to_roadmap(self):
        expected_list = [(self.test_object_one, 1), (self.test_object_two, 1), (self.test_object_three, 1)]

        add_request = self.factory.post('/roadmaps/view_roadmap/add/?id=' + str(self.test_roadmap.id), {
            'procedure': [self.test_object_one.id, self.test_object_two.id, self.test_object_three.id], 'phase': 1})

        add_request.user = self.user
        self.middleware.process_request(add_request)
        add_request.session.save()

        response = add_to_roadmap(add_request)

        self.assertEqual(response.status_code, 302)

        self.assertListEqual(expected_list, RoadmapProcedureLink.get_procedures_from_roadmap(self.test_roadmap))

    def test_add_to_roadmap_invalid_id(self):
        expected_list = []

        add_request = self.factory.post('/roadmaps/view_roadmap/add/?id=' + str(99999), {
            'procedure': [self.test_object_one.id, self.test_object_two.id, self.test_object_three.id], 'phase': 1})

        add_request.user = self.user
        self.middleware.process_request(add_request)
        add_request.session.save()

        setattr(add_request, 'session', 'session')
        messages = FallbackStorage(add_request)
        setattr(add_request, '_messages', messages)

        response = add_to_roadmap(add_request)

        self.assertEqual(response.status_code, 302)

        self.assertListEqual(expected_list, RoadmapProcedureLink.get_procedures_from_roadmap(self.test_roadmap))

    def test_add_to_roadmap_invalid_form(self):
        expected_list = []

        add_request = self.factory.post('/roadmaps/view_roadmap/add/?id=' + str(self.test_roadmap.id), {
            'procedure': [self.test_object_one.id, self.test_object_two.id, self.test_object_three.id]})

        add_request.user = self.user
        self.middleware.process_request(add_request)
        add_request.session.save()

        setattr(add_request, 'session', 'session')
        messages = FallbackStorage(add_request)
        setattr(add_request, '_messages', messages)

        response = add_to_roadmap(add_request)

        self.assertEqual(response.status_code, 302)

        self.assertListEqual(expected_list, RoadmapProcedureLink.get_procedures_from_roadmap(self.test_roadmap))

    def test_remove_from_roadmap(self):
        self.test_add_to_roadmap()

        # Remove procedure one and three from the roadmap
        remove_request = self.factory.post('/roadmaps/view_roadmap/remove/?id=' + str(self.test_roadmap.id), {
            'selection[]': ['1,1', '3,1']
        })

        remove_request.user = self.user
        self.middleware.process_request(remove_request)

        response = remove_selected_pairs(remove_request)

        self.assertEqual(response.status_code, 302)

        expected_list = [(self.test_object_two, 1)]

        self.assertListEqual(expected_list, RoadmapProcedureLink.get_procedures_from_roadmap(self.test_roadmap))

    def test_remove_nothing_from_roadmap(self):
        self.test_add_to_roadmap()

        # Remove procedure one and three from the roadmap
        remove_request = self.factory.post('/roadmaps/view_roadmap/remove/?id=' + str(self.test_roadmap.id), {
            'selection[]': []
        })

        remove_request.user = self.user
        self.middleware.process_request(remove_request)

        response = remove_selected_pairs(remove_request)

        self.assertEqual(response.status_code, 302)

        expected_list = [(self.test_object_one, 1), (self.test_object_two, 1), (self.test_object_three, 1)]

        self.assertListEqual(expected_list, RoadmapProcedureLink.get_procedures_from_roadmap(self.test_roadmap))

    def test_remove_from_roadmap_invalid_roadmap_id(self):
        self.test_add_to_roadmap()

        # Remove procedure one and three from the roadmap
        remove_request = self.factory.post('/roadmaps/view_roadmap/remove/?id=' + str(99999), {
            'selection[]': ['1,1', '3,1']
        })

        remove_request.user = self.user
        self.middleware.process_request(remove_request)

        setattr(remove_request, 'session', 'session')
        messages = FallbackStorage(remove_request)
        setattr(remove_request, '_messages', messages)

        response = remove_selected_pairs(remove_request)

        self.assertEqual(response.status_code, 302)

        expected_list = [(self.test_object_one, 1), (self.test_object_two, 1), (self.test_object_three, 1)]

        self.assertListEqual(expected_list, RoadmapProcedureLink.get_procedures_from_roadmap(self.test_roadmap))

    def test_delete_roadmap(self):
        self.test_add_to_roadmap()

        # Delete the roadmap
        delete_request = self.factory.post('/roadmaps/view_roadmap/delete/?id=' + str(self.test_roadmap.id),
                                           {'item_name': str(self.test_roadmap.roadmap_name)})

        delete_request.user = self.user
        self.middleware.process_request(delete_request)

        response = delete_roadmap(delete_request)

        self.assertEqual(response.status_code, 302)

        expected_list = []

        # Assert there are no procedure-phase pairs since they've been deleted
        self.assertListEqual(expected_list, RoadmapProcedureLink.get_procedures_from_roadmap(self.test_roadmap))

        # Assert the roadmap itself no longer exists
        self.assertListEqual(expected_list, list(Roadmap.objects.filter(id=self.test_roadmap.id)))

    def test_delete_roadmap_name_mismatch(self):
        self.test_add_to_roadmap()

        # Delete the roadmap
        delete_request = self.factory.post('/roadmaps/view_roadmap/delete/?id=' + str(self.test_roadmap.id),
                                           {'item_name': str(self.test_roadmap.roadmap_name) + "bad text"})

        delete_request.user = self.user
        self.middleware.process_request(delete_request)

        setattr(delete_request, 'session', 'session')
        messages = FallbackStorage(delete_request)
        setattr(delete_request, '_messages', messages)

        response = delete_roadmap(delete_request)

        self.assertEqual(response.status_code, 302)

        expected_pair_list = [(self.test_object_one, 1), (self.test_object_two, 1), (self.test_object_three, 1)]

        expected_roadmap_list = [self.test_roadmap]

        # Assert there are no procedure-phase pairs since they've been deleted
        self.assertListEqual(expected_pair_list, RoadmapProcedureLink.get_procedures_from_roadmap(self.test_roadmap))

        # Assert the roadmap itself no longer exists
        self.assertListEqual(expected_roadmap_list, list(Roadmap.objects.filter(id=self.test_roadmap.id)))

    def test_delete_roadmap_invalid_form(self):
        self.test_add_to_roadmap()

        # Delete the roadmap
        delete_request = self.factory.post('/roadmaps/view_roadmap/delete/?id=' + str(self.test_roadmap.id),
                                           {})

        delete_request.user = self.user
        self.middleware.process_request(delete_request)

        setattr(delete_request, 'session', 'session')
        messages = FallbackStorage(delete_request)
        setattr(delete_request, '_messages', messages)

        response = delete_roadmap(delete_request)

        self.assertEqual(response.status_code, 302)

        expected_pair_list = [(self.test_object_one, 1), (self.test_object_two, 1), (self.test_object_three, 1)]

        expected_roadmap_list = [self.test_roadmap]

        # Assert there are no procedure-phase pairs since they've been deleted
        self.assertListEqual(expected_pair_list, RoadmapProcedureLink.get_procedures_from_roadmap(self.test_roadmap))

        # Assert the roadmap itself no longer exists
        self.assertListEqual(expected_roadmap_list, list(Roadmap.objects.filter(id=self.test_roadmap.id)))

    def test_delete_roadmap_invalid_roadmap_id(self):
        self.test_add_to_roadmap()

        # Delete the roadmap
        delete_request = self.factory.post('/roadmaps/view_roadmap/delete/?id=' + str(99999),
                                           {'item_name': str(self.test_roadmap.roadmap_name)})

        delete_request.user = self.user
        self.middleware.process_request(delete_request)

        setattr(delete_request, 'session', 'session')
        messages = FallbackStorage(delete_request)
        setattr(delete_request, '_messages', messages)

        response = delete_roadmap(delete_request)

        self.assertEqual(response.status_code, 302)

        expected_pair_list = [(self.test_object_one, 1), (self.test_object_two, 1), (self.test_object_three, 1)]

        expected_roadmap_list = [self.test_roadmap]

        # Assert there are no procedure-phase pairs since they've been deleted
        self.assertListEqual(expected_pair_list, RoadmapProcedureLink.get_procedures_from_roadmap(self.test_roadmap))

        # Assert the roadmap itself no longer exists
        self.assertListEqual(expected_roadmap_list, list(Roadmap.objects.filter(id=self.test_roadmap.id)))

    def test_update_roadmap_valid(self):
        request = self.factory.post('/roadmaps/view_roadmap/update/?id=' + str(self.test_roadmap.id),
                                    {'roadmap_name': 'Updated Roadmap', 'time_frame': 'days', 'time': '22'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = update_roadmap(request)
        self.assertEqual(response.status_code, 302)

        test_roadmap = Roadmap.objects.get(roadmap_name='Updated Roadmap')
        self.assertIsNotNone(test_roadmap)

    def test_update_roadmap_invalid_form(self):
        request = self.factory.post('/roadmaps/view_roadmap/update/?id=' + str(self.test_roadmap.id),
                                    {'roadmap_name': 'Updated Roadmap', 'time': '22'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = update_roadmap(request)
        self.assertEqual(response.status_code, 302)

        # If an entry exists, it will overwrite None, thus failing the test
        try:
            test_roadmap = None
            test_roadmap = Roadmap.objects.get(roadmap_name='Updated Roadmap')
        except Roadmap.DoesNotExist:
            self.assertIsNone(test_roadmap)

    def test_update_roadmap_valid_invalid_roadmap_id(self):
        request = self.factory.post('/roadmaps/view_roadmap/update/?id=' + str(99999),
                                    {'roadmap_name': 'Updated Roadmap', 'time_frame': 'days', 'time': '22'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = update_roadmap(request)
        self.assertEqual(response.status_code, 302)

        # If an entry exists, it will overwrite None, thus failing the test
        try:
            test_roadmap = None
            test_roadmap = Roadmap.objects.get(roadmap_name='Updated Roadmap')
        except Roadmap.DoesNotExist:
            self.assertIsNone(test_roadmap)
