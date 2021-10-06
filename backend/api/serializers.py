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


# TO FIX COURSE SERIALIZER CREATE()
class CourseSerializer(serializers.ModelSerializer):
    instructors = StaffAccountSerializer()

    class Meta:
        model = Course
        fields = ['name', 'hours', 'class_type', 'points_value', 'instructors']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['index', 'email', 'name', 'surname']


class StudentIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['index']


class FieldOfStudySerializer(serializers.ModelSerializer):
    #students = StudentIndexSerializer()
    #students = serializers.JSONField()

    class Meta:
        model = FieldOfStudy
        fields = ['name', 'study_type', 'start_date', 'end_date', 'students']

    def create(self, validated_data):
        student_list = validated_data.get('students')
        field_of_study = FieldOfStudy(name=validated_data.get('name'), study_type=validated_data.get('study_type'))
        if validated_data.get('start_date') is not None:
            field_of_study.start_date = validated_data.get('start_date')
        if validated_data.get('end_date') is not None:
            field_of_study.end_date=validated_data.get('end_date')
        field_of_study.save()
        for i in student_list:
            if Student.objects.filter(index=i.index).exists():
                field_of_study.students.add(i)
        field_of_study.save()
        return field_of_study


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['name', 'capacity', 'room_type']
