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
        fields = ['id', 'name', 'points_value', 'course_instructor_info']

    # def create(self, validated_data):
    #     course_instructor_info = validated_data.get('course_instructor_info')
    #     if CourseInstructorInfo.objects.filter(id=course_instructor_info).exists():
    #         course_inst_info_instance = CourseInstructorInfo.objects.get(id=course_instructor_info)
    #         course = Course(course_instructor_info=course_inst_info_instance,
    #                         name=validated_data.get('name'),
    #                         points_value=validated_data.get('points_value'))
    #         course_instructor_info.save()
    #         return course


class CourseInstructorInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseInstructorInfo
        fields = ['id', 'instructor', 'course_type', 'hours']

    # def create(self, validated_data):
    #     instructor = validated_data.get('instructor')
    #     if StaffAccount.objects.filter(id=instructor).exists():
    #         instructor_instance = StaffAccount.objects.get(id=instructor)
    #         courseinstrinfo = CourseInstructorInfo(course_type=validated_data.get('course_type'),
    #                                                hours=validated_data.get('hours'),
    #                                                instructor=instructor_instance)
    #         courseinstrinfo.save()
    #         return courseinstrinfo


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'index', 'email', 'name', 'surname']


class FieldOfStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldOfStudy
        fields = ['id', 'name', 'study_type', 'start_date', 'end_date', 'students']

    # def create(self, validated_data):
    #     student_list = validated_data.get('students')
    #     field_of_study = FieldOfStudy(name=validated_data.get('name'), study_type=validated_data.get('study_type'))
    #     if validated_data.get('start_date') is not None:
    #         field_of_study.start_date = validated_data.get('start_date')
    #     if validated_data.get('end_date') is not None:
    #         field_of_study.end_date = validated_data.get('end_date')
    #     field_of_study.save()
    #     for i in student_list:
    #         if Student.objects.filter(id=i.id).exists():
    #             field_of_study.students.add(i)
    #     field_of_study.save()
    #     return field_of_study


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'capacity', 'room_type']



class ECTSCardSerializer(serializers.ModelSerializer):
    # TODO overwrite create() method for instructors list after staff-register fix
    class Meta:
        model = ECTSCard
        fields = ['courses', 'field_of_study', 'semester', 'year']


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['id', 'semester', 'year', 'students', 'field_of_study', 'courses']

    # def create(self, validated_data):
    #     student_list = validated_data.get('students')
    #     courses_list = validated_data.get('courses')
    #     semester = Semester(name=validated_data.get('name'), study_type=validated_data.get('study_type'))
    #     semester.save()
    #     for i in student_list:
    #         if Student.objects.filter(id=i.id).exists():
    #             semester.students.add(i)
    #     semester.save()
    #
    #     for i in courses_list:
    #         if Course.objects.filter(id=i.id).exists():
    #             semester.courses.add(i)
    #     semester.save()
    #
    #     return semester
