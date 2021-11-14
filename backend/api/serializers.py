from rest_framework import serializers
from api.models import (
    Student,
    Course,
    FieldOfStudy,
    Room,
    ECTSCard,
    CourseInstructorInfo,
    Semester
)
from accounts.models import User, StaffAccount, DeaneryAccount
from accounts.serializers import UserSerializer


class StaffUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class StaffAccountSerializer(serializers.ModelSerializer):
    user = StaffUserSerializer()

    class Meta:
        model = StaffAccount
        fields = ['user', 'name', 'surname', 'institute', 'job_title', 'academic_title']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'points_value', 'course_instructor_info', 'name']


class CourseInstructorInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseInstructorInfo
        fields = ['id', 'instructor', 'course_type', 'hours']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'index', 'email', 'name', 'surname']


class FieldOfStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldOfStudy
        fields = ['id', 'name', 'study_type', 'start_date', 'end_date', 'students']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'capacity', 'room_type']


class ECTSCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ECTSCard
        fields = ['id', 'courses', 'field_of_study', 'semester']


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['id', 'semester', 'year', 'students', 'field_of_study', 'courses']
