from config.settings import SEMESTER_COURSES_POINTS_LIMIT
from django.db.models import Sum
from rest_framework import serializers
from api.models import (
    Student,
    Course,
    FieldOfStudy,
    Room,
    ECTSCard,
    CourseInstructorInfo,
    Semester,
    FieldGroup,
    TimeTable,
    TimeTableUnit
)
from accounts.models import User
from accounts.serializers import UserSerializer

from accounts.serializers import StaffAccountSerializer


class StaffUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'points_value', 'name', 'prerequisites', 'purposes',
                  'subject_learning_outcomes', 'methods_of_verification_of_learning_outcomes_and_criteria',
                  'content_of_the_subject', 'didactic_methods', 'literature', 'balance_of_work_of_an_avg_student']


class CourseGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'points_value', 'name', 'prerequisites', 'purposes',
                  'subject_learning_outcomes', 'methods_of_verification_of_learning_outcomes_and_criteria',
                  'content_of_the_subject', 'didactic_methods', 'literature', 'balance_of_work_of_an_avg_student']


class CourseInstructorInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseInstructorInfo
        fields = ['id', 'instructor', 'course_type', 'hours', 'course']

    def validate_instructor(self, instance):
        instructor_current_courses_hours = CourseInstructorInfo.objects.filter(instructor=instance).aggregate(Sum('hours'))['hours__sum']
        if instructor_current_courses_hours is not None:
            if instructor_current_courses_hours > instance.pensum_hours:
                raise serializers.ValidationError("Pracownik przekracza sumaryczną ilość godzin pracy.")
        return instance

class CourseInstructorInfoGetSerializer(serializers.ModelSerializer):
    instructor = StaffAccountSerializer()
    course = CourseGetSerializer()

    class Meta:
        model = CourseInstructorInfo
        fields = ['id', 'instructor', 'course_type', 'hours', 'course']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'index', 'email', 'name', 'surname']


class RoomSerializer(serializers.ModelSerializer):
    room_type = serializers.ListField()

    class Meta:
        model = Room
        fields = ['id', 'name', 'capacity', 'room_type']


class FieldGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldGroup
        fields = ['id', 'name']


class FieldOfStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldOfStudy
        fields = ['id', 'name', 'study_type', 'start_date', 'end_date', 'field_groups']


class FieldOfStudyGetSerializer(serializers.ModelSerializer):
    field_groups = FieldGroupSerializer(many=True)

    class Meta:
        model = FieldOfStudy
        fields = ['id', 'name', 'study_type', 'start_date', 'end_date', 'field_groups']


class SemesterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Semester
        fields = ['id', 'semester', 'year', 'students', 'field_of_study', 'courses',
                  'semester_start_date', 'semester_end_date']

    def validate_courses(self, data):
        sum = 0
        [sum := sum + x.points_value for x in data]
        if sum > SEMESTER_COURSES_POINTS_LIMIT:
            raise serializers.ValidationError("Semestr przekracza dozwoloną ilość punktów w przedmiotach (30).")
        return data

class SemesterGetSerializer(serializers.ModelSerializer):
    courses = CourseGetSerializer(many=True)
    students = StudentSerializer(many=True)

    class Meta:
        model = Semester
        fields = ['id', 'semester', 'year', 'students', 'field_of_study', 'courses',
                  'semester_start_date', 'semester_end_date']


class ECTSCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ECTSCard
        fields = ['id', 'field_of_study', 'semester']


class ECTSCardGetSerializer(serializers.ModelSerializer):
    field_of_study = FieldOfStudyGetSerializer()
    semester = SemesterSerializer()

    class Meta:
        model = ECTSCard
        fields = ['id', 'field_of_study', 'semester']


class TimeTableUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTableUnit
        fields = ['id', 'day', 'start_hour', 'end_hour', 'week', 'course_instructor_info', 'field_groups', 'room']


class TimeTableUnitGetSerializer(serializers.ModelSerializer):
    course_instructor_info = CourseInstructorInfoGetSerializer()
    field_groups = FieldGroupSerializer(many=True)
    room = RoomSerializer()

    class Meta:
        model = TimeTableUnit
        fields = ['id', 'day', 'start_hour', 'end_hour', 'week', 'course_instructor_info', 'field_groups', 'room']


class TimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = ['id', 'semester', 'time_table_units']


class TimeTableGetSerializer(serializers.ModelSerializer):
    semester = SemesterGetSerializer()
    time_table_units = TimeTableUnitGetSerializer(many=True)

    class Meta:
        model = TimeTable
        fields = ['id', 'semester', 'time_table_units']


class TimeTableWithTimeTableUnitsSerializer(serializers.Serializer):
    semester = serializers.IntegerField()
    time_table_unit = TimeTableUnitSerializer()


class TimeTableWithTimeTableUnitsGetSerializer(serializers.Serializer):
    semester = serializers.IntegerField()
    time_table_unit = TimeTableUnitGetSerializer(many=True)
