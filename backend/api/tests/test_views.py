from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import (
    Student,
    Room,
    FieldGroup,
    FieldOfStudy,
    CourseInstructorInfo,
    Course,
    Semester,
    ECTSCard,
    TimeTableUnit,
    TimeTable
)
from django.urls import reverse
from rest_framework.test import APITestCase
from .test_setup import TestSetUp


class TestViews(TestSetUp):

    def test_student_get_post(self):
        response = self.client.post(self.student_url, self.student_data, format='json')
        email = self.student_data['email']

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Student.objects.get().email, email)
        