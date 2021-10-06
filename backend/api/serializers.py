from rest_framework import serializers
from api.models import Student, Course, FieldOfStudy, Room
from accounts.models import User, StaffAccount, DeaneryAccount
from accounts.serializers import UserSerializer


class DeanUserSerializer(serializers.ModelSerializer):
    pass


class StaffUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class StaffAccountSerializer(serializers.ModelSerializer):
    user = StaffUserSerializer()

    class Meta:
        model = StaffAccount
        fields = ['user', 'name', 'surname', 'institute', 'job_title', 'academic_title']


#TO FIX COURSE SERIALIZER CREATE()
class CourseSerializer(serializers.ModelSerializer):
    instructors = StaffAccountSerializer()

    class Meta:
        model = Course
        fields = ['name', 'hours', 'class_type', 'points_value', 'instructors']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['index', 'email', 'name', 'surname']


class FieldOfStudySerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True)

    class Meta:
        model = FieldOfStudy
        fields = ['name', 'study_type', 'start_date', 'end_date', 'students']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['name', 'capacity', 'room_type']