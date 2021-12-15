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
from accounts.models import User, StaffAccount, DeaneryAccount
from accounts.serializers import UserSerializer

from accounts.serializers import StaffAccountSerializer


class StaffUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class CourseInstructorInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseInstructorInfo
        fields = ['id', 'instructor', 'course_type', 'hours']


class CourseInstructorInfoGetSerializer(serializers.ModelSerializer):
    instructor = StaffAccountSerializer()

    class Meta:
        model = CourseInstructorInfo
        fields = ['id', 'instructor', 'course_type', 'hours']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['points_value', 'course_instructor_info', 'name', 'prerequisites', 'purposes',
                  'subject_learning_outcomes', 'methods_of_verification_of_learning_outcomes_and_criteria',
                  'content_of_the_subject', 'didactic_methods', 'literature', 'balance_of_work_of_an_avg_student']


class CourseGetSerializer(serializers.ModelSerializer):
    course_instructor_info = CourseInstructorInfoGetSerializer(many=True)

    class Meta:
        model = Course
        fields = ['points_value', 'course_instructor_info', 'name', 'prerequisites', 'purposes',
                  'subject_learning_outcomes', 'methods_of_verification_of_learning_outcomes_and_criteria',
                  'content_of_the_subject', 'didactic_methods', 'literature', 'balance_of_work_of_an_avg_student']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'index', 'email', 'name', 'surname']


class RoomSerializer(serializers.ModelSerializer):
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
        fields = ['id', 'courses', 'field_of_study', 'semester']


class ECTSCardGetSerializer(serializers.ModelSerializer):
    courses = CourseGetSerializer(many=True)
    field_of_study = FieldOfStudyGetSerializer()
    semester = SemesterSerializer()

    class Meta:
        model = ECTSCard
        fields = ['id', 'courses', 'field_of_study', 'semester']


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
