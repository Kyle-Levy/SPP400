from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User

from .views import log_in

# Create your tests here.
class TestLogin(TestCase):

    #create setUp so every test can have access to the requestFactory
    def setUp(self):
        self.factory = RequestFactory()


    def test_login_page(self):
        user = User.objects.create_user('testuser', 'testuser@email.com', 'super_secret_pass')
        user.save()

        request = self.factory.post('login/', {'username': 'testuser', 'password': 'super_secret_pass'})
        response = log_in(request)
        print(response)



