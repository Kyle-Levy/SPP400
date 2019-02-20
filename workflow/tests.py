from django.contrib.auth.models import User
from django.test import TestCase
from viewflow.models import Process


class Test(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.client.login(username='admin', password='password')

    def testApproved(self):
        self.client.post(
            '/workflow/workflow/workflow/start/',
            {
                'text': 'urine test',
                '_viewflow_activation-started': '2019-01-01'
            }
        )

        self.client.post(
            '/workflow/workflow/workflow/1/approve/2/assign/'
        )

        self.client.post(
            'workflow/workflow/workflow/1/approve/2/',
            {
                'approved': True,
                '_viewflow_activation-started': '2019-01-01'
            }
        )

        process = Process.objects.get()

        self.assertEquals('NEW', process.status)
        self.assertEquals(2, process.task_set.count())

    def testNotApproved(self):
        self.client.post(
            '/workflow/workflow/workflow/start/',
            {
                'text': 'urine test',
                '_viewflow_activation-started': '2019-01-01'
            }
        )

        self.client.post(
            '/workflow/workflow/workflow/1/approve/2/assign/'
        )

        self.client.post(
            'workflow/workflow/workflow/1/approve/2/',
            {
                'approved': False,
                '_viewflow_activation-started': '2019-01-01'
            }
        )

        process = Process.objects.get()

        self.assertEquals('NEW', process.status)
        self.assertEquals(2, process.task_set.count())
