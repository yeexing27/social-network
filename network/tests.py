from django.http import response
from django.test import TestCase, Client
from .models import User, Post, Comment, Follow

# Create your tests here.


class NetworkTestCase(TestCase):

    def test_post_number(self):
        """Check the presence of variable 'selected' """

        c = Client()
        response = c.get("")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["selected"], 1)
