from django.test import TestCase
from django.test import Client


# Create your tests here.
class BasicTest(TestCase):

    def setUp(self):
        pass

    def test_get_home(self):
        c = Client()
        response = c.get('/')
        response_str = response.content.decode('utf-8')
        self.assertEqual(response_str, '8INF958 Basic demo')
