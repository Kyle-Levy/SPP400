from django.test import RequestFactory, TestCase
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User
from procedures.views import new_procedure
from roadmaps.views import roadmaps_index, create_roadmap, view_roadmap, add_to_roadmap, remove_selected_pairs, \
    delete_roadmap
from .models import Procedure, Roadmap, RoadmapProcedureLink


class TestProcedures(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware()
        self.user = User.objects.create_superuser('testuser', 'testuser@email.com', 'supersecretpass')
        self.user.save()

        # Creating procedures for testing the ability to add them to a roadmap
        request = self.factory.post('create/', {'procedure_name': 'Object One', 'notes': 'These are test notes', 'time_frame': 'days', 'time': '22'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        new_procedure(request)
        self.test_object_one = Procedure.objects.get(procedure_name='Object One',
                                                     procedure_info='These are test notes')

        # Creating procedures for testing the ability to add them to a roadmap
        request = self.factory.post('create/', {'procedure_name': 'Object Two', 'notes': 'These are test notes', 'time_frame': 'days', 'time': '22'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        new_procedure(request)
        self.test_object_two = Procedure.objects.get(procedure_name='Object Two',
                                                     procedure_info='These are test notes')

        # Creating procedures for testing the ability to add them to a roadmap
        request = self.factory.post('create/', {'procedure_name': 'Object Three', 'notes': 'These are test notes', 'time_frame': 'days', 'time': '22'})
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        new_procedure(request)
        self.test_object_three = Procedure.objects.get(procedure_name='Object Three',
                                                       procedure_info='These are test notes')

        request = self.factory.post('/roadmaps/create/', {'roadmap_name': 'Test Roadmap', 'time_frame': 'days', 'time': '22'})
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
        request = self.factory.post('/roadmaps/create/', {'roadmap_name': 'Created Roadmap', 'time_frame': 'days', 'time': '22'})
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

        response = create_roadmap(request)
        self.assertEqual(response.status_code, 401)

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

        response = view_roadmap(request)

        self.assertEqual(response.status_code, 302)

    def test_post_view_roadmap_valid(self):
        request = self.factory.post('/roadmaps/view_roadmap/?id=' + str(self.test_roadmap.id))
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = view_roadmap(request)

        self.assertEqual(response.status_code, 200)

    def test_post_view_roadmap_invalid(self):
        request = self.factory.post('/roadmaps/view_roadmap/?id=' + str(self.test_roadmap.id + 99999))
        request.user = self.user
        self.middleware.process_request(request)
        request.session.save()

        response = view_roadmap(request)

        self.assertEqual(response.status_code, 302)

    def test_add_to_roadmap(self):
        # View roadmap first
        view_request = self.factory.post('/roadmaps/view_roadmap/?id=' + str(self.test_roadmap.id))
        view_request.user = self.user
        self.middleware.process_request(view_request)
        view_request.session.save()

        response = view_roadmap(view_request)

        self.assertEqual(response.status_code, 200)

        expected_list = [(self.test_object_one, 1), (self.test_object_two, 1), (self.test_object_three, 1)]

        add_request = self.factory.post('/roadmaps/view_roadmap/add/', {
            'procedure': [self.test_object_one.id, self.test_object_two.id, self.test_object_three.id], 'phase': 1})

        add_request.user = self.user
        add_request.session = view_request.session

        response = add_to_roadmap(add_request)

        self.assertEqual(response.status_code, 200)

        self.assertListEqual(expected_list, RoadmapProcedureLink.get_procedures_from_roadmap(self.test_roadmap))

    def test_add_to_roadmap_invalid_id(self):
        # View roadmap first
        view_request = self.factory.post('/roadmaps/view_roadmap/?id=' + str(self.test_roadmap.id))
        view_request.user = self.user
        self.middleware.process_request(view_request)
        view_request.session.save()

        response = view_roadmap(view_request)

        self.assertEqual(response.status_code, 200)

        add_request = self.factory.post('/roadmaps/view_roadmap/add/', {
            'procedure': [self.test_object_one.id, self.test_object_two.id, self.test_object_three.id], 'phase': 1})

        add_request.user = self.user
        add_request.session = view_request.session

        add_request.session['roadmap_id'] = 99999
        response = add_to_roadmap(add_request)

        self.assertEqual(response.status_code, 302)

    def test_add_to_roadmap_invalid_form(self):
        # View roadmap first
        view_request = self.factory.post('/roadmaps/view_roadmap/?id=' + str(self.test_roadmap.id))
        view_request.user = self.user
        self.middleware.process_request(view_request)
        view_request.session.save()

        response = view_roadmap(view_request)

        self.assertEqual(response.status_code, 200)

        add_request = self.factory.post('/roadmaps/view_roadmap/add/', {
            'procedure': [self.test_object_one.id, self.test_object_two.id, self.test_object_three.id]})

        add_request.user = self.user
        add_request.session = view_request.session

        response = add_to_roadmap(add_request)

        self.assertEqual(response.status_code, 302)

    def test_remove_from_roadmap(self):
        # View roadmap first
        view_request = self.factory.post('/roadmaps/view_roadmap/?id=' + str(self.test_roadmap.id))
        view_request.user = self.user
        self.middleware.process_request(view_request)
        view_request.session.save()

        response = view_roadmap(view_request)

        self.assertEqual(response.status_code, 200)

        expected_list = [(self.test_object_one, 1), (self.test_object_two, 1), (self.test_object_three, 1)]

        # Add procedure one, two, and three to phase one
        add_request = self.factory.post('/roadmaps/view_roadmap/add/', {
            'procedure': [self.test_object_one.id, self.test_object_two.id, self.test_object_three.id], 'phase': 1})

        add_request.user = self.user
        add_request.session = view_request.session

        response = add_to_roadmap(add_request)

        self.assertEqual(response.status_code, 200)

        self.assertListEqual(expected_list, RoadmapProcedureLink.get_procedures_from_roadmap(self.test_roadmap))

        # Remove procedure one and three from the roadmap
        remove_request = self.factory.post('/roadmaps/view_roadmap/remove/', {
            'selection[]': ['1,1', '3,1']
        })

        remove_request.user = self.user
        remove_request.session = view_request.session

        response = remove_selected_pairs(remove_request)

        self.assertEqual(response.status_code, 200)

        expected_list = [(self.test_object_two, 1)]

        self.assertListEqual(expected_list, RoadmapProcedureLink.get_procedures_from_roadmap(self.test_roadmap))

    def test_remove_nothing_from_roadmap(self):
        # View roadmap first
        view_request = self.factory.post('/roadmaps/view_roadmap/?id=' + str(self.test_roadmap.id))
        view_request.user = self.user
        self.middleware.process_request(view_request)
        view_request.session.save()

        response = view_roadmap(view_request)

        self.assertEqual(response.status_code, 200)

        expected_list = [(self.test_object_one, 1), (self.test_object_two, 1), (self.test_object_three, 1)]

        # Add procedure one, two, and three to phase one
        add_request = self.factory.post('/roadmaps/view_roadmap/add/', {
            'procedure': [self.test_object_one.id, self.test_object_two.id, self.test_object_three.id], 'phase': 1})

        add_request.user = self.user
        add_request.session = view_request.session

        response = add_to_roadmap(add_request)

        self.assertEqual(response.status_code, 200)

        self.assertListEqual(expected_list, RoadmapProcedureLink.get_procedures_from_roadmap(self.test_roadmap))

        # Remove procedure one and three from the roadmap
        remove_request = self.factory.post('/roadmaps/view_roadmap/remove/', {
            'selection[]': []
        })

        remove_request.user = self.user
        remove_request.session = view_request.session

        response = remove_selected_pairs(remove_request)

        self.assertEqual(response.status_code, 200)

        self.assertListEqual(expected_list, RoadmapProcedureLink.get_procedures_from_roadmap(self.test_roadmap))

    def test_remove_from_roadmap_invalid_roadmap_id(self):
        # View roadmap first
        view_request = self.factory.post('/roadmaps/view_roadmap/?id=' + str(self.test_roadmap.id))
        view_request.user = self.user
        self.middleware.process_request(view_request)
        view_request.session.save()

        response = view_roadmap(view_request)

        self.assertEqual(response.status_code, 200)

        expected_list = [(self.test_object_one, 1), (self.test_object_two, 1), (self.test_object_three, 1)]

        # Add procedure one, two, and three to phase one
        add_request = self.factory.post('/roadmaps/view_roadmap/add/', {
            'procedure': [self.test_object_one.id, self.test_object_two.id, self.test_object_three.id], 'phase': 1})

        add_request.user = self.user
        add_request.session = view_request.session

        response = add_to_roadmap(add_request)

        self.assertEqual(response.status_code, 200)

        self.assertListEqual(expected_list, RoadmapProcedureLink.get_procedures_from_roadmap(self.test_roadmap))

        # Remove procedure one and three from the roadmap
        remove_request = self.factory.post('/roadmaps/view_roadmap/remove/', {
            'selection[]': []
        })

        remove_request.user = self.user
        remove_request.session = view_request.session
        remove_request.session['roadmap_id'] = 99999

        response = remove_selected_pairs(remove_request)

        self.assertEqual(response.status_code, 302)

    def test_delete_roadmap(self):
        # View roadmap first
        view_request = self.factory.post('/roadmaps/view_roadmap/?id=' + str(self.test_roadmap.id))
        view_request.user = self.user
        self.middleware.process_request(view_request)
        view_request.session.save()

        response = view_roadmap(view_request)

        self.assertEqual(response.status_code, 200)

        expected_list = [(self.test_object_one, 1), (self.test_object_two, 1), (self.test_object_three, 1)]

        # Add procedure one, two, and three to phase one
        add_request = self.factory.post('/roadmaps/view_roadmap/add/', {
            'procedure': [self.test_object_one.id, self.test_object_two.id, self.test_object_three.id], 'phase': 1})

        add_request.user = self.user
        add_request.session = view_request.session

        response = add_to_roadmap(add_request)

        self.assertEqual(response.status_code, 200)

        self.assertListEqual(expected_list, RoadmapProcedureLink.get_procedures_from_roadmap(self.test_roadmap))

        # Delete the roadmap
        delete_request = self.factory.post('/roadmaps/view_roadmap/delete/')

        delete_request.user = self.user
        delete_request.session = view_request.session

        response = delete_roadmap(delete_request)

        self.assertEqual(response.status_code, 302)

        expected_list = []

        # Assert there are no procedure-phase pairs since they've been deleted
        self.assertListEqual(expected_list, RoadmapProcedureLink.get_procedures_from_roadmap(self.test_roadmap))

        # Assert the roadmap itself no longer exists
        self.assertListEqual(expected_list, list(Roadmap.objects.filter(id=self.test_roadmap.id)))

    def test_delete_roadmap_bad_id(self):
        # View roadmap first
        view_request = self.factory.post('/roadmaps/view_roadmap/?id=' + str(self.test_roadmap.id))
        view_request.user = self.user
        self.middleware.process_request(view_request)
        view_request.session.save()

        response = view_roadmap(view_request)

        self.assertEqual(response.status_code, 200)

        expected_list = [(self.test_object_one, 1), (self.test_object_two, 1), (self.test_object_three, 1)]

        # Add procedure one, two, and three to phase one
        add_request = self.factory.post('/roadmaps/view_roadmap/add/', {
            'procedure': [self.test_object_one.id, self.test_object_two.id, self.test_object_three.id], 'phase': 1})

        add_request.user = self.user
        add_request.session = view_request.session

        response = add_to_roadmap(add_request)

        self.assertEqual(response.status_code, 200)

        self.assertListEqual(expected_list, RoadmapProcedureLink.get_procedures_from_roadmap(self.test_roadmap))

        # Delete the roadmap
        delete_request = self.factory.post('/roadmaps/view_roadmap/delete/')

        delete_request.user = self.user
        delete_request.session = view_request.session

        # Fudge the roadmap_id stored
        delete_request.session['roadmap_id'] = 99999

        response = delete_roadmap(delete_request)

        self.assertEqual(response.status_code, 302)

        # Assert the list did not change since they weren't deleted
        self.assertListEqual(expected_list, RoadmapProcedureLink.get_procedures_from_roadmap(self.test_roadmap))

        expected_roadmap_list = [self.test_roadmap]
        # Assert the roadmap itself no longer exists
        self.assertListEqual(expected_roadmap_list, list(Roadmap.objects.filter(id=self.test_roadmap.id)))