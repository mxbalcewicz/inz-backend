from django.test import TestCase

#Third-party app imports
from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key

# Relative imports of the 'app-name' package
from api.models import Course

class KidTestModel(TestCase):
    """
    Class to test the model Course
    """

    # def setUp(self):
    #     """
    #     Set up all the tests
    #     """
    #     self.course = mommy.make(Course)

    def test_model_creation_course(self):
        new_course = mommy.make(Course)
        self.assertTrue(isinstance(new_course, Course))
        
