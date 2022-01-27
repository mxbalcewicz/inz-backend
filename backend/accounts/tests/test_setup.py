from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetUp(APITestCase):

    def setUp(self):
        """
        Set up all the tests
        """
        self.register_staff_url = reverse()
