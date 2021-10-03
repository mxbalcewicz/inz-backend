from rest_framework import serializers
from api.models import Student


class CourseSerializer(serializers.ModelSerializer):
    #TODO STAFF SERIALIZERS (ACCOUNTS)
    pass


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'email', 'name', 'surname']


class FieldOfStudySerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True)

    class Meta:
        fields = ['study_type', 'start_date', 'students']

