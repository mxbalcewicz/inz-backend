from django.urls import reverse
from rest_framework.test import APITestCase


class TestSetUp(APITestCase):

    def setUp(self):
        self.student_url = reverse('student_get_post')
        self.courseinstructorinfo_url =  reverse('courseinstructorinfo_get_post')
        self.course_url = reverse('course_get_post')      
        self.room_url = reverse('room_get_post')
        self.fieldofstudy_url = reverse('fieldofstudy_get_post')
        self.semester_url = reverse('semester_get_post')
        self.ectscard_url = reverse('ectscard_get_post')
        self.fieldgroup_url = reverse('field_group_get_post')
        self.timetable_url = reverse('timetable_get_post')
        self.timetableunit_url = reverse('timetableunit_get_post')

        self.student_data = {
            'index': 12345,
            'email': 'testemail@mail.com',
            'name': 'TestName',
            'surname': 'TestSurname'
        }

    def tearDown(self):
        pass
