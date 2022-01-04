from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers, viewsets, status
from rest_framework.views import APIView
import pandas as pd
import json

from .models import (Student,
                     FieldOfStudy,
                     Course,
                     Room,
                     ECTSCard,
                     Student,
                     CourseInstructorInfo,
                     Semester,
                     FieldGroup,
                     TimeTable,
                     TimeTableUnit
                     )
from accounts.models import StaffAccount
from .serializers import (StudentSerializer,
                          StaffAccountSerializer,
                          FieldOfStudySerializer,
                          CourseSerializer,
                          RoomSerializer,
                          ECTSCardSerializer,
                          CourseInstructorInfoSerializer,
                          SemesterSerializer,
                          FieldGroupSerializer,
                          TimeTableSerializer, TimeTableUnitSerializer, FieldOfStudyGetSerializer,
                          ECTSCardGetSerializer, SemesterGetSerializer, TimeTableUnitGetSerializer,
                          TimeTableGetSerializer, CourseInstructorInfoGetSerializer, CourseGetSerializer,
                          )
from django.http import HttpResponse
import csv


class StaffUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StaffAccount.objects.all()
    serializer_class = StaffAccountSerializer


class RoomGetPostView(APIView):
    """
    Room get, post view
    """
    serializer_class = RoomSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        rooms = Room.objects.all()
        serializer = self.serializer_class(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoomRetrieveUpdateDeleteView(APIView):
    """
    Room retrieve, update, delete view
    """
    serializer_class = RoomSerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        instance = get_object_or_404(Room, pk=pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        instance = Room.objects.get(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = Room.objects.get(pk=pk)
        instance.name = request.data.get('name')
        instance.capacity = request.data.get('capacity')
        instance.room_type = request.data.get('room_type')
        instance.save()
        updated_instance = Room.objects.get(pk=pk)
        serializer = self.serializer_class(updated_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentGetPostView(APIView):
    """
    Student get, post view
    """
    serializer_class = StudentSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        students = Student.objects.all()
        serializer = self.serializer_class(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentRetrieveUpdateDeleteView(APIView):
    """
    Student retrieve, update, delete view
    """
    serializer_class = StudentSerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        instance = get_object_or_404(Student, pk=pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        instance = Student.objects.get(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = Student.objects.get(pk=pk)
        instance.name = request.data.get('name')
        instance.surname = request.data.get('surname')
        instance.index = request.data.get('index')
        instance.email = request.data.get('email')
        instance.save()
        updated_instance = Student.objects.get(pk=pk)
        serializer = self.serializer_class(updated_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseInstructorInfoGetPostView(APIView):
    """
    CourseInstructorInfo get, post view
    """
    serializer_class = CourseInstructorInfoSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        instructor_info_list = CourseInstructorInfo.objects.all()
        serializer = CourseInstructorInfoGetSerializer(instructor_info_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseInstructorInfoRetrieveUpdateDeleteView(APIView):
    """
    CourseInstructorInfo retrieve, update, delete view
    """
    serializer_class = CourseInstructorInfoSerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        instance = get_object_or_404(CourseInstructorInfo, pk=pk)
        serializer = CourseInstructorInfoGetSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        instance = CourseInstructorInfo.objects.get(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = CourseInstructorInfo.objects.get(pk=pk)
        instructor_id = request.data.get('instructor')
        course_id = request.data.get('course')
        if StaffAccount.objects.filter(pk=instructor_id).exists() and Course.objects.filter(pk=course_id):
            instructor_instance = StaffAccount.objects.get(pk=instructor_id)
            instance.instructor = instructor_instance
            course_instance = Course.objects.get(pk=course_id)
            instance.course = course_instance
            instance.hours = request.data.get('hours')
            instance.course_type = request.data.get('course_type')
            instance.save()
            updated_instance = CourseInstructorInfo.objects.get(pk=pk)
            serializer = self.serializer_class(updated_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)


class CourseGetPostView(APIView):
    """
    Course get, post view
    """
    serializer_class = CourseSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        course = Course(name=request.data.get('name'), points_value=request.data.get('points_value'))
        if request.data.get('prerequisites') is not None:
            course.prerequisites = request.data.get('prerequisites')
        if request.data.get('subject_learning_outcomes') is not None:
            course.subject_learning_outcomes = request.data.get('subject_learning_outcomes')
        if request.data.get('purposes') is not None:
            course.purposes = request.data.get('purposes')
        if request.data.get('methods_of_verification_of_learning_outcomes_and_criteria') is not None:
            course.methods_of_verification_of_learning_outcomes_and_criteria = request.data.get(
                'methods_of_verification_of_learning_outcomes_and_criteria')
        if request.data.get('content_of_the_subject') is not None:
            course.content_of_the_subject = request.data.get('content_of_the_subject')
        if request.data.get('didactic_methods') is not None:
            course.didactic_methods = request.data.get('didactic_methods')
        if request.data.get('literature') is not None:
            course.literature = request.data.get('literature')
        if request.data.get('balance_of_work_of_an_avg_student') is not None:
            course.balance_of_work_of_an_avg_student = request.data.get('balance_of_work_of_an_avg_student')
        course.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        course_list = Course.objects.all()
        serializer = CourseGetSerializer(course_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseRetrieveUpdateDeleteView(APIView):
    """
    Course retrieve, update, delete view
    """
    serializer_class = CourseSerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        instance = get_object_or_404(Course, pk=pk)
        serializer = CourseGetSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        instance = Course.objects.get(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = Course.objects.get(pk=pk)

        if request.data.get('points_value') is not None:
            instance.points_value = request.data.get('points_value')
        if request.data.get('name') is not None:
            instance.name = request.data.get('name')
        if request.data.get('prerequisites') is not None:
            instance.prerequisites = request.data.get('prerequisites')
        if request.data.get('purposes') is not None:
            instance.purposes = request.data.get('purposes')
        if request.data.get('subject_learning_outcomes') is not None:
            instance.subject_learning_outcomes = request.data.get('subject_learning_outcomes')
        if request.data.get('methods_of_verification_of_learning_outcomes_and_criteria') is not None:
            instance.methods_of_verification_of_learning_outcomes_and_criteria = request.data.get(
                'methods_of_verification_of_learning_outcomes_and_criteria')
        if request.data.get('content_of_the_subject') is not None:
            instance.content_of_the_subject = request.data.get('content_of_the_subject')
        if request.data.get('didactic_methods') is not None:
            instance.didactic_methods = request.data.get('didactic_methods')
        if request.data.get('literature') is not None:
            instance.literature = request.data.get('literature')
        if request.data.get('balance_of_work_of_an_avg_student') is not None:
            instance.balance_of_work_of_an_avg_student = request.data.get('balance_of_work_of_an_avg_student')

        instance.save()
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FieldOfStudyGetPostView(APIView):
    """
    FieldOfStudy get, post view
    """
    serializer_class = FieldOfStudySerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        field_of_study = FieldOfStudy(
            name=request.data.get('name'),
            study_type=request.data.get('study_type'),
            start_date=request.data.get('start_date'),
            end_date=request.data.get('end_date')
        )
        field_of_study.save()

        field_groups = request.data.get('field_groups')
        for i in field_groups:
            if FieldGroup.objects.filter(id=i).exists():
                temp = FieldGroup.objects.get(id=i)
                field_of_study.field_groups.add(temp)
                field_of_study.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        field_of_study_list = FieldOfStudy.objects.all()
        serializer = FieldOfStudyGetSerializer(field_of_study_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FieldOfStudyRetrieveUpdateDeleteView(APIView):
    """
    FieldOfStudy retrieve, update, delete view
    """
    serializer_class = FieldOfStudySerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        instance = get_object_or_404(FieldOfStudy, pk=pk)
        serializer = FieldOfStudyGetSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        instance = FieldOfStudy.objects.get(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = FieldOfStudy.objects.get(pk=pk)

        instance.name = request.data.get('name')
        instance.start_date = request.data.get('start_date')
        instance.end_date = request.data.get('end_date')
        instance.study_type = request.data.get('study_type')
        field_groups = request.data.get('field_groups')
        instance.field_groups.clear()

        for i in field_groups:
            if FieldGroup.objects.filter(id=i):
                temp = FieldGroup.objects.get(id=i)
                instance.field_groups.add(temp)
                instance.save()

        updated_instance = FieldOfStudy.objects.get(pk=pk)
        serializer = self.serializer_class(updated_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SemesterGetPostView(APIView):
    """
    Semester get, post view
    """
    serializer_class = SemesterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        fieldofstudy_id = request.data.get('field_of_study')
        if FieldOfStudy.objects.filter(id=fieldofstudy_id).exists():
            fieldofstudy = FieldOfStudy.objects.get(id=fieldofstudy_id)

            semester = Semester(
                year=request.data.get('year'),
                semester=request.data.get('semester'),
                field_of_study=fieldofstudy,
                semester_start_date=request.data.get('semester_start_date'),
                semester_end_date=request.data.get('semester_end_date')
            )
            semester.save()

            students = request.data.get('students')
            for i in students:
                if Student.objects.filter(id=i).exists():
                    student = Student.objects.get(id=i)
                    semester.students.add(student)
                    semester.save()

            courses = request.data.get('courses')
            for i in courses:
                if Course.objects.filter(id=i).exists():
                    course = Course.objects.get(id=i)
                    semester.courses.add(course)
                    semester.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        semester = Semester.objects.all()
        serializer = SemesterGetSerializer(semester, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SemesterRetrieveUpdateDeleteView(APIView):
    """
    Semester retrieve, update, delete view
    """
    serializer_class = SemesterSerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        instance = get_object_or_404(Semester, pk=pk)
        serializer = SemesterGetSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        instance = Semester.objects.get(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = Semester.objects.get(pk=pk)

        instance.year = request.data.get('year')
        instance.semester = request.data.get('semester')
        instance.semester_start_date = request.data.get('semester_start_date')
        instance.semester_end_date = request.data.get('semester_end_date')
        courses = request.data.get('courses')
        students = request.data.get('students')

        instance.courses.clear()
        instance.students.clear()

        for i in students:
            if Student.objects.filter(id=i).exists():
                student = Student.objects.get(id=i)
                instance.students.add(student)
                instance.save()

        for i in courses:
            if Course.objects.filter(id=i).exists():
                course = Course.objects.get(id=i)
                instance.courses.add(course)
                instance.save()

        if FieldOfStudy.objects.filter(id=request.data.get('field_of_study')).exists():
            temp = FieldOfStudy.objects.get(id=request.data.get('field_of_study'))
            instance.field_of_study = temp

        updated_instance = Semester.objects.get(pk=pk)
        serializer = self.serializer_class(updated_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ECTSCardGetPostView(APIView):
    """
    ECTSCard get, post view
    """
    serializer_class = ECTSCardSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        ectscard = ECTSCard.objects.all()
        serializer = ECTSCardGetSerializer(ectscard, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ECTSCardRetrieveUpdateDeleteView(APIView):
    """
    ECTSCard retrieve, update, delete view
    """
    serializer_class = ECTSCardSerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        instance = get_object_or_404(ECTSCard, pk=pk)
        serializer = ECTSCardGetSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        instance = ECTSCard.objects.get(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = ECTSCard.objects.get(pk=pk)

        fieldofstudy_id = request.data.get('field_of_study')
        semester_id = request.data.get('semester')
        if FieldOfStudy.objects.filter(id=fieldofstudy_id).exists() and Semester.objects.filter(
                id=semester_id).exists():
            fieldofstudy = FieldOfStudy.objects.get(id=fieldofstudy_id)
            semester = Semester.objects.get(id=semester_id)
            instance.field_of_study = fieldofstudy
            instance.semester = semester
            instance.save()

        updated_instance = ECTSCard.objects.get(pk=pk)
        serializer = self.serializer_class(updated_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FieldGroupGetPostView(APIView):
    """
    FieldGroup get, post view
    """
    serializer_class = FieldGroupSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        field_group = FieldGroup.objects.all()
        serializer = self.serializer_class(field_group, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FieldGroupRetrieveUpdateDeleteView(APIView):
    """
    FieldGroup retrieve, update, delete view
    """
    serializer_class = FieldGroupSerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        instance = get_object_or_404(FieldGroup, pk=pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        instance = FieldGroup.objects.get(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        if FieldGroup.objects.filter(pk=pk).exists():
            field_group_instance = FieldGroup.objects.get(pk=pk)
            field_group_instance.name = request.data.get('name')
            field_group_instance.save()
            updated_instance = FieldGroup.objects.get(pk=pk)
            serializer = self.serializer_class(updated_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TimeTableUnitGetPostView(APIView):
    """
    TimeTableUnit get, post view
    """
    serializer_class = TimeTableUnitSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        course_instructor_info_id = request.data.get('course_instructor_info')
        if Room.objects.filter(id=request.data.get('room')).exists() is False:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        if CourseInstructorInfo.objects.filter(id=course_instructor_info_id).exists():
            course_inst_info = CourseInstructorInfo.objects.get(id=course_instructor_info_id)
            room = Room.objects.get(id=request.data.get("room"))
            time_table_unit = TimeTableUnit(course_instructor_info=course_inst_info,
                                            start_hour=request.data.get('start_hour'),
                                            end_hour=request.data.get('end_hour'),
                                            day=request.data.get('day'),
                                            week=request.data.get('week'),
                                            room=room)
            time_table_unit.save()
            field_groups = request.data.get('field_groups')
            for i in field_groups:
                if FieldGroup.objects.filter(id=i).exists():
                    temp = FieldGroup.objects.get(id=i)
                    time_table_unit.field_groups.add(temp)
                    time_table_unit.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        time_table_unit = TimeTableUnit.objects.all()
        serializer = TimeTableUnitGetSerializer(time_table_unit, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TimeTableUnitRetrieveUpdateDeleteView(APIView):
    """
    TimeTableUnit retrieve, update, delete view
    """
    serializer_class = TimeTableUnitSerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        instance = get_object_or_404(TimeTableUnit, pk=pk)
        serializer = TimeTableUnitGetSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        instance = TimeTableUnit.objects.get(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        course_inst_info_id = request.data.get('course_instructor_info')
        room_id = request.data.get('room')
        if TimeTableUnit.objects.filter(id=pk).exists() and CourseInstructorInfo.objects.filter(
                id=course_inst_info_id).exists() and Room.objects.filter(id=room_id).exists():
            instance = TimeTableUnit.objects.get(pk=pk)
            course_inst_info = CourseInstructorInfo.objects.get(id=course_inst_info_id)
            instance.course_instructor_info = course_inst_info
            instance.room = Room.objects.get(pk=room_id)
            instance.day = request.data.get('day')
            instance.week = request.data.get('week')
            instance.start_hour = request.data.get('start_hour')
            instance.end_hour = request.data.get('end_hour')
            instance.field_groups.clear()
            instance.save()
            field_groups = request.data.get('field_groups')

            for i in field_groups:
                if FieldGroup.objects.filter(id=i).exists():
                    temp = FieldGroup.objects.get(id=i)
                    instance.field_groups.add(temp)
                    instance.save()

            updated_instance = TimeTableUnit.objects.get(pk=pk)
            serializer = self.serializer_class(updated_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TimeTableGetPostView(APIView):
    """
    TimeTable get, post view
    """
    serializer_class = TimeTableSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        semester_id = request.data.get('semester')
        if Semester.objects.filter(id=semester_id).exists():
            semester = Semester.objects.get(id=semester_id)
            time_table = TimeTable(
                semester=semester
            )
            time_table.save()

            time_table_units = request.data.get('time_table_units')
            for i in time_table_units:
                if TimeTableUnit.objects.filter(id=i).exists():
                    temp = TimeTableUnit.objects.get(id=i)
                    time_table.time_table_units.add(temp)
                    time_table.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        time_table = TimeTable.objects.all()
        serializer = TimeTableGetSerializer(time_table, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TimeTableRetrieveUpdateDeleteView(APIView):
    """
    TimeTable retrieve, update, delete view
    """
    serializer_class = TimeTableSerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        instance = get_object_or_404(TimeTable, pk=pk)
        serializer = TimeTableGetSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        instance = TimeTable.objects.get(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = TimeTable.objects.get(pk=pk)
        semester_id = request.data.get('semester')
        if Semester.objects.filter(id=semester_id).exists():
            semester = Semester.objects.get(id=semester_id)
            instance.semester = semester
            instance.time_table_units.clear()
            instance.save()

            time_table_units = request.data.get('time_table_units')
            for i in time_table_units:
                if TimeTableUnit.objects.filter(id=i).exists():
                    temp = TimeTableUnit.objects.get(id=i)
                    instance.time_table_units.add(temp)
                    instance.save()

            updated_instance = TimeTable.objects.get(pk=pk)
            serializer = self.serializer_class(updated_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TimeTableWithTimeTableUnitsPostView(APIView):

    def post(self, request):
        semester_id = request.data.get('semester')
        time_table_units = request.data.get('time_table_units')
        if semester_id is None:
            return Response("No semester in json data", status=status.HTTP_400_BAD_REQUEST)
        if time_table_units is None:
            return Response("No time table units in json data", status=status.HTTP_400_BAD_REQUEST)
        semester = Semester.objects.filter(pk=semester_id).first()
        if semester is None:
            return Response("There is no semester with given id", status=status.HTTP_400_BAD_REQUEST)

        time_table = TimeTable(
            semester=semester
        )
        time_table.save()

        for i in time_table_units:
            serializer = TimeTableUnitSerializer(data=i)
            serializer.is_valid(raise_exception=True)

            course_instructor_info_id = i['course_instructor_info']

            if Room.objects.filter(id=i['room']).exists() is False:
                return Response("there is no room with given id", status=status.HTTP_400_BAD_REQUEST)
            if CourseInstructorInfo.objects.filter(id=course_instructor_info_id).exists():
                course_inst_info = CourseInstructorInfo.objects.get(id=course_instructor_info_id)
                room = Room.objects.filter(id=i['room']).first()
                time_table_unit = TimeTableUnit(course_instructor_info=course_inst_info,
                                                start_hour=i['start_hour'],
                                                end_hour=i['end_hour'],
                                                day=i['day'],
                                                week=i['week'],
                                                room=room)
                time_table_unit.save()
                field_groups = i['field_groups']
                for j in field_groups:
                    if FieldGroup.objects.filter(id=j).exists():
                        temp = FieldGroup.objects.get(id=j)
                        time_table_unit.field_groups.add(temp)
                        time_table_unit.save()
                        time_table.time_table_units.add(time_table_unit)
                        time_table.save()

        return Response(status=status.HTTP_200_OK)


class TimeTableWithTimeTableUnitsUpdateView(APIView):

    def put(self, request, pk):
        semester_id = request.data.get('semester')
        time_table_units = request.data.get('time_table_units')
        if semester_id is None:
            return Response("No semester in json data", status=status.HTTP_400_BAD_REQUEST)
        if time_table_units is None:
            return Response("No time table units in json data", status=status.HTTP_400_BAD_REQUEST)
        semester = Semester.objects.filter(pk=semester_id).first()
        if semester is None:
            return Response("There is no semester with given id", status=status.HTTP_400_BAD_REQUEST)

        time_table = TimeTable.objects.filter(pk=pk).first()
        if time_table is None:
            return Response("There is no time table with given id", status=status.HTTP_400_BAD_REQUEST)
        time_table.semester = semester
        time_table.save()
        time_table.time_table_units.clear()

        for i in time_table_units:
            serializer = TimeTableUnitSerializer(data=i)
            serializer.is_valid(raise_exception=True)

            course_instructor_info_id = i['course_instructor_info']

            if Room.objects.filter(id=i['room']).exists() is False:
                return Response("there is no room with given id", status=status.HTTP_400_BAD_REQUEST)
            if CourseInstructorInfo.objects.filter(id=course_instructor_info_id).exists():
                course_inst_info = CourseInstructorInfo.objects.get(id=course_instructor_info_id)
                room = Room.objects.filter(id=i['room']).first()

                time_table_unit = TimeTableUnit(course_instructor_info=course_inst_info,
                                                start_hour=i['start_hour'],
                                                end_hour=i['end_hour'],
                                                day=i['day'],
                                                week=i['week'],
                                                room=room)
                time_table_unit.save()
                field_groups = i['field_groups']
                for j in field_groups:
                    if FieldGroup.objects.filter(id=j).exists():
                        temp = FieldGroup.objects.get(id=j)
                        time_table_unit.field_groups.add(temp)
                        time_table_unit.save()
                        time_table.time_table_units.add(time_table_unit)
                        time_table.save()

        return Response(status=status.HTTP_200_OK)


class StudentsCSVExportView(APIView):
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Students.csv"'

        serializer = self.serializer_class(Student.objects.all(), many=True)
        header = self.serializer_class.Meta.fields

        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)

        return response


class CourseInstructorInfosCSVExportView(APIView):
    serializer_class = CourseInstructorInfoSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Students.csv"'

        serializer = self.serializer_class(CourseInstructorInfo.objects.all(), many=True)
        header = self.serializer_class.Meta.fields

        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)

        return response


class RoomsCSVExportView(APIView):
    serializer_class = RoomSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Rooms.csv"'

        serializer = self.serializer_class(
            Room.objects.all(),
            many=True
        )
        header = self.serializer_class.Meta.fields

        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)

        return response


class CourseCSVExportView(APIView):
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Courses.csv"'

        serializer = self.serializer_class(
            Course.objects.all(),
            many=True
        )
        header = self.serializer_class.Meta.fields

        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)

        return response


class CourseInstructorInfoCSVExportView(APIView):
    serializer_class = CourseInstructorInfoSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="CourseInstructorInfos.csv"'

        serializer = self.serializer_class(
            CourseInstructorInfo.objects.all(),
            many=True
        )
        header = self.serializer_class.Meta.fields

        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)

        return response


class SemesterCSVExportView(APIView):
    serializer_class = SemesterSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Semesters.csv"'

        serializer = self.serializer_class(
            Semester.objects.all(),
            many=True
        )
        header = self.serializer_class.Meta.fields

        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)

        return response


class FieldGroupCSVExportView(APIView):
    serializer_class = FieldGroupSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="FieldGroup.csv"'

        serializer = self.serializer_class(
            FieldGroup.objects.all(),
            many=True
        )
        header = self.serializer_class.Meta.fields

        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)

        return response


class FieldOfStudyCSVExportView(APIView):
    serializer_class = FieldOfStudySerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="FieldOfStudy.csv"'

        serializer = self.serializer_class(
            FieldOfStudy.objects.all(),
            many=True
        )
        header = self.serializer_class.Meta.fields

        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)

        return response


class ECTSCardCSVExportView(APIView):
    serializer_class = ECTSCardSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="ECTSCard.csv"'

        serializer = self.serializer_class(
            ECTSCard.objects.all(),
            many=True
        )
        header = self.serializer_class.Meta.fields

        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)

        return response


class TimeTableUnitCSVExportView(APIView):
    serializer_class = TimeTableUnitSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="TimeTableUnit.csv"'

        serializer = self.serializer_class(
            TimeTableUnit.objects.all(),
            many=True
        )
        header = self.serializer_class.Meta.fields

        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)

        return response


class TimeTableCSVExportView(APIView):
    serializer_class = TimeTableSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="TimeTable.csv"'

        serializer = self.serializer_class(
            TimeTable.objects.all(),
            many=True
        )
        header = self.serializer_class.Meta.fields

        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)

        return response


class RoomCSVImportView(APIView):

    def post(self, request):
        file = pd.read_csv(request.FILES['files'], sep=',', header=0)

        for index, row in file.iterrows():
            if row['name'] and row['id'] and row['capacity'] and row['room_type'] is not None:
                if Room.objects.filter(id=row['id']).exists() is False:
                    room = Room(id=row['id'],
                                name=row['name'],
                                capacity=row['capacity'],
                                room_type=row['room_type'])
                else:
                    room = Room.objects.filter(id=row['id']).first()
                    room.name = row['name']
                    room.capacity = row['capacity']
                    room.room_type = row['room_type']
                room.save()

        return Response(status=status.HTTP_200_OK)


class CourseCSVImportView(APIView):

    def post(self, request):
        file = pd.read_csv(request.FILES['files'], sep=',', header=0)

        for index, row in file.iterrows():
            if row['name'] and row['points_value'] and row['id'] is not None:
                course = Course.objects.filter(id=row['id']).first()
                if course is not None:
                    course.name = row['name']
                    course.points_value = row['points_value']
                else:
                    course = Course(id=row['id'], name=row['name'], points_value=row['points_value'])

                if row['prerequisites'] is not None:
                    course.prerequisites = row['prerequisites']
                if row['subject_learning_outcomes'] is not None:
                    course.subject_learning_outcomes = row['subject_learning_outcomes']
                if row['purposes'] is not None:
                    course.purposes = row['purposes']
                if row['methods_of_verification_of_learning_outcomes_and_criteria'] is not None:
                    course.methods_of_verification_of_learning_outcomes_and_criteria = row[
                        'methods_of_verification_of_learning_outcomes_and_criteria']
                if row['content_of_the_subject'] is not None:
                    course.content_of_the_subject = row['content_of_the_subject']
                if row['didactic_methods'] is not None:
                    course.didactic_methods = row['didactic_methods']
                if row['literature'] is not None:
                    course.literature = row['literature']
                if row['balance_of_work_of_an_avg_student'] is not None:
                    course.balance_of_work_of_an_avg_student = row['balance_of_work_of_an_avg_student']
                course.save()

        return Response(status=status.HTTP_200_OK)


class CourseInstructorInfosCSVImportView(APIView):

    def post(self, request):
        file = pd.read_csv(request.FILES['files'], sep=',', header=0)

        for index, row in file.iterrows():
            if row['id'] is not None:
                courseinstinfo = CourseInstructorInfo.objects.filter(id=row['id']).first()
                if courseinstinfo is not None:
                    courseinstinfo.hours = row['hours']
                    courseinstinfo.course_type = row['course_type']
                    instructor = StaffAccount.objects.filter(pk=row['instructor']).first()
                    if instructor is not None:
                        courseinstinfo.instructor = instructor
                    course = Course.objects.get(pk=row['course'])
                    if course is not None:
                        courseinstinfo.course = course
                    courseinstinfo.save()
                else:
                    if Course.objects.filter(pk=row['course']).exists() and \
                            StaffAccount.objects.filter(pk=row['instructor']).exists() is not False:
                        if row['course_type'] and row['hours'] is not None:
                            courseinstinfo = CourseInstructorInfo(id=row['id'],
                                                                  hours=row['hours'],
                                                                  course_type=row['course_type'],
                                                                  instructor=StaffAccount.objects.get(
                                                                      pk=row['instructor']),
                                                                  course=Course.objects.get(pk=row['course']))
                            courseinstinfo.save()

        return Response(status=status.HTTP_200_OK)


class StudentsCSVImportView(APIView):

    def post(self, request):
        file = pd.read_csv(request.FILES['files'], sep=',', header=0)

        for index, row in file.iterrows():
            if row['id'] is not None:
                student = Student.objects.filter(id=row['id']).first()
            if student is not None:
                if row['index'] and row['email'] and row['name'] and row['surname'] is not None:
                    student.index = row['index']
                    student.email = row['email']
                    student.name = row['name']
                    student.surname = row['surname']
                    student.save()
            else:
                if row['index'] and row['email'] and row['name'] and row['surname'] is not None:
                    if Student.objects.filter(index=row['index']).exists() is False:
                        if Student.objects.filter(email=row['email']).exists() is False:
                            student = Student(id=row['id'],
                                              index=row['index'],
                                              email=row['email'],
                                              name=row['name'],
                                              surname=row['surname'])
                            student.save()

        return Response(status=status.HTTP_200_OK)


class SemesterCSVImportView(APIView):

    def post(self, request):

        file = pd.read_csv(request.FILES['files'], sep=',', header=0)

        for index, row in file.iterrows():
            if row['id'] is not None:
                semester = Semester.objects.filter(id=row['id']).first()
                if row['semester'] and row['year'] and row['students'] and row['field_of_study'] and \
                        row['courses'] and row['semester_start_date'] and row['semester_end_date'] is not None:
                    if semester is not None:
                        semester.year = row['year']
                        semester.semester = row['semester']
                        fieldofstudy = FieldOfStudy.objects.filter(id=row['field_of_study']).first()
                        if fieldofstudy is not None:
                            semester.field_of_study = fieldofstudy
                        semester.semester_start_date = row['semester_start_date']
                        semester.semester_end_date = row['semester_end_date']
                        semester.save()
                        students = convertStringCSVArrtoArr(row['students'])

                        for i in students:
                            if Student.objects.filter(id=i).exists():
                                student = Student.objects.get(id=i)
                                semester.students.add(student)
                                semester.save()

                        courses = convertStringCSVArrtoArr(row['courses'])

                        for i in courses:
                            if Course.objects.filter(id=i).exists():
                                course = Course.objects.get(id=i)
                                semester.courses.add(course)
                                semester.save()
                        semester.save()
                    else:
                        fieldofstudy_id = row['field_of_study']
                        if FieldOfStudy.objects.filter(id=fieldofstudy_id).exists():
                            fieldofstudy = FieldOfStudy.objects.get(id=fieldofstudy_id)

                            semester = Semester(
                                id=row['id'],
                                year=row['year'],
                                semester=row['semester'],
                                field_of_study=fieldofstudy,
                                semester_start_date=row['semester_start_date'],
                                semester_end_date=row['semester_end_date']
                            )
                            semester.save()
                            students = convertStringCSVArrtoArr(row['students'])

                            for i in students:
                                if Student.objects.filter(id=i).exists():
                                    student = Student.objects.get(id=i)
                                    semester.students.add(student)
                                    semester.save()

                            courses = convertStringCSVArrtoArr(row['courses'])

                            for i in courses:
                                if Course.objects.filter(id=i).exists():
                                    course = Course.objects.get(id=i)
                                    semester.courses.add(course)
                                    semester.save()
                            semester.save()

        return Response(status=status.HTTP_200_OK)


class FieldGroupCSVImportView(APIView):

    def post(self, request):
        file = pd.read_csv(request.FILES['files'], sep=',', header=0)

        for index, row in file.iterrows():
            if row['name'] and row['id'] is not None:
                field_group = FieldGroup.objects.filter(id=row['id']).first()
                if field_group is not None:
                    field_group.name = row['name']
                else:
                    field_group = FieldGroup(id=row['id'], name=row['name'])
                field_group.save()
        return Response(status=status.HTTP_200_OK)


class FieldOfStudyCSVImportView(APIView):

    def post(self, request):
        file = pd.read_csv(request.FILES['files'], sep=',', header=0)

        for index, row in file.iterrows():
            if row['id'] and row['name'] and row['study_type'] and row['start_date'] and row['end_date'] \
                    and row['field_groups'] is not None:
                field_of_study = FieldOfStudy.objects.filter(id=row['id']).first()
                if field_of_study is None:
                    field_of_study = FieldOfStudy(id=row['id'],
                                                  name=row['name'],
                                                  study_type=row['study_type'],
                                                  start_date=row['start_date'],
                                                  end_date=row['end_date'])
                else:
                    field_of_study.name = row['name']
                    field_of_study.study_type = row['study_type']
                    field_of_study.start_date = row['start_date']
                    field_of_study.end_date = row['end_date']

                field_of_study.save()
                field_groups = convertStringCSVArrtoArr(row['field_groups'])

                for i in field_groups:
                    if FieldGroup.objects.filter(pk=i).exists():
                        temp = FieldGroup.objects.get(pk=i)
                        field_of_study.field_groups.add(temp)
                        field_of_study.save()

        return Response(status=status.HTTP_200_OK)


class ECTSCardCSVImportView(APIView):

    def post(self, request):
        file = pd.read_csv(request.FILES['files'], sep=',', header=0)

        for index, row in file.iterrows():
            field_of_study_id = row['field_of_study']
            semester_id = row['semester']
            if row['id'] and field_of_study_id and semester_id is not None:
                semester = Semester.objects.filter(pk=semester_id).first()
                field_of_study = FieldOfStudy.objects.filter(pk=field_of_study_id).first()
                if semester or field_of_study is None:
                    ects_card = ECTSCard.objects.filter(id=row['id']).first()
                    if ects_card is not None:
                        ects_card.semester = semester
                        ects_card.field_of_study = field_of_study
                    else:
                        ects_card = ECTSCard(id=row['id'], semester=semester, field_of_study=field_of_study)
                    ects_card.save()

        return Response(status=status.HTTP_200_OK)


class TimeTableCSVImportView(APIView):
    def post(self, request):
        file = pd.read_csv(request.FILES['files'], sep=',', header=0)

        for index, row in file.iterrows():
            semester_id = row['semester']
            time_table_units = row['time_table_units']
            semester = Semester.objects.filter(pk=semester_id).first()
            if semester or time_table_units or row['id'] is None:
                time_table = TimeTable.objects.filter(id=row['id']).first()
                if time_table is None:
                    time_table = TimeTable(id=row['id'], semester=semester)
                else:
                    time_table.semester = semester
                time_table.save()
                time_table_units = convertStringCSVArrtoArr(time_table_units)

                for i in time_table_units:
                    if TimeTableUnit.objects.filter(id=i).exists():
                        temp = TimeTableUnit.objects.get(id=i)
                        time_table.time_table_units.add(temp)
                        time_table.save()
        return Response(status=status.HTTP_200_OK)


class TimeTableUnitCSVImportView(APIView):
    def post(self, request):
        file = pd.read_csv(request.FILES['files'], sep=',', header=0)

        for index, row in file.iterrows():
            day = row['day']
            start_hour = row['start_hour']
            end_hour = row['end_hour']
            week = row['week']
            course_instructor_info_id = row['course_instructor_info']
            field_groups = row['field_groups']
            room_id = row['room']
            if row[
                'id'] or day or start_hour or end_hour or week or course_instructor_info_id or field_groups or room_id is None:
                room = Room.objects.filter(pk=room_id).first()
                course_instructor_info = CourseInstructorInfo.objects.filter(pk=course_instructor_info_id).first()
                if room or course_instructor_info is None:
                    time_table_unit = TimeTableUnit.objects.filter(id=row['id']).first()
                    if time_table_unit is not None:
                        time_table_unit.day = day
                        time_table_unit.start_hour = start_hour
                        time_table_unit.end_hour = end_hour
                        time_table_unit.week = week
                        time_table_unit.room = room
                        time_table_unit.course_instructor_info = course_instructor_info
                    else:
                        time_table_unit = TimeTableUnit(id=row['id'],
                                                        day=day,
                                                        start_hour=start_hour,
                                                        end_hour=end_hour,
                                                        week=week,
                                                        room=room,
                                                        course_instructor_info=course_instructor_info)
                    time_table_unit.save()
                    field_groups = convertStringCSVArrtoArr(field_groups)
                    for i in field_groups:
                        if FieldGroup.objects.filter(id=i).exists():
                            temp = FieldGroup.objects.get(id=i)
                            time_table_unit.field_groups.add(temp)
                            time_table_unit.save()

        return Response(status=status.HTTP_200_OK)


def convertStringCSVArrtoArr(csvStr):
    res = csvStr
    res = res.replace("[", "")
    res = res.replace("]", "")
    res = res.replace(",", "")
    res = res.split()
    return res


class StudentsJSONExportView(APIView):
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/json')
        response['Content-Disposition'] = 'attachment; filename="Students.json"'
        serializer = self.serializer_class(Student.objects.all(), many=True)
        data = json.dumps(serializer.data)
        response.write(data)
        return response


class StaffJSONExportView(APIView):
    serializer_class = StaffAccountSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/json')
        response['Content-Disposition'] = 'attachment; filename="Staff.json"'
        serializer = self.serializer_class(StaffAccount.objects.all(), many=True)
        data = json.dumps(serializer.data)
        response.write(data)
        return response


class RoomsJSONExportView(APIView):
    serializer_class = RoomSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/json')
        response['Content-Disposition'] = 'attachment; filename="Rooms.json"'
        serializer = self.serializer_class(Room.objects.all(), many=True)
        data = json.dumps(serializer.data)
        response.write(data)
        return response


class CourseJSONExportView(APIView):
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/json')
        response['Content-Disposition'] = 'attachment; filename="Courses.json"'
        serializer = self.serializer_class(Course.objects.all(), many=True)
        data = json.dumps(serializer.data)
        response.write(data)
        return response


class CourseInstructorInfosJSONExportView(APIView):
    serializer_class = CourseInstructorInfoSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/json')
        response['Content-Disposition'] = 'attachment; filename="CourseInstructorInfos.json"'
        serializer = self.serializer_class(CourseInstructorInfo.objects.all(), many=True)
        data = json.dumps(serializer.data)
        response.write(data)
        return response


class SemesterJSONExportView(APIView):
    serializer_class = SemesterSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/json')
        response['Content-Disposition'] = 'attachment; filename="Semester.json"'
        serializer = self.serializer_class(Semester.objects.all(), many=True)
        data = json.dumps(serializer.data)
        response.write(data)
        return response


class FieldGroupJSONExportView(APIView):
    serializer_class = FieldGroupSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/json')
        response['Content-Disposition'] = 'attachment; filename="FieldGroup.json"'
        serializer = self.serializer_class(FieldGroup.objects.all(), many=True)
        data = json.dumps(serializer.data)
        response.write(data)
        return response


class FieldOfStudyJSONExportView(APIView):
    serializer_class = FieldOfStudySerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/json')
        response['Content-Disposition'] = 'attachment; filename="FieldOfStudy.json"'
        serializer = self.serializer_class(FieldOfStudy.objects.all(), many=True)
        data = json.dumps(serializer.data)
        response.write(data)
        return response


class TimeTableJSONExportView(APIView):
    serializer_class = TimeTableSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/json')
        response['Content-Disposition'] = 'attachment; filename="TimeTable.json"'
        serializer = self.serializer_class(TimeTable.objects.all(), many=True)
        data = json.dumps(serializer.data)
        response.write(data)
        return response


class TimeTableUnitJSONExportView(APIView):
    serializer_class = TimeTableUnitSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/json')
        response['Content-Disposition'] = 'attachment; filename="TimeTableUnit.json"'
        serializer = self.serializer_class(TimeTableUnit.objects.all(), many=True)
        data = json.dumps(serializer.data)
        response.write(data)
        return response


class ECTSCardJSONExportView(APIView):
    serializer_class = ECTSCardSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/json')
        response['Content-Disposition'] = 'attachment; filename="ECTSCard.json"'
        serializer = self.serializer_class(ECTSCard.objects.all(), many=True)
        data = json.dumps(serializer.data)
        response.write(data)
        return response


class StudentsJSONImportView(APIView):
    serializer_class = StudentSerializer

    def post(self, request):
        file = json.load(request.FILES['files'])
        for row in file:
            if row['id'] is not None:
                student = Student.objects.filter(id=row['id']).first()
            if student is not None:
                if row['index'] and row['email'] and row['name'] and row['surname'] is not None:
                    student.index = row['index']
                    student.email = row['email']
                    student.name = row['name']
                    student.surname = row['surname']
                    student.save()
            else:
                if row['index'] and row['email'] and row['name'] and row['surname'] is not None:
                    if Student.objects.filter(index=row['index']).exists() is False:
                        if Student.objects.filter(email=row['email']).exists() is False:
                            student = Student(id=row['id'],
                                              index=row['index'],
                                              email=row['email'],
                                              name=row['name'],
                                              surname=row['surname'])
                            student.save()

        return Response(status=status.HTTP_200_OK)


class RoomJSONImportView(APIView):
    serializer_class = RoomSerializer

    def post(self, request):
        file = json.load(request.FILES['files'])
        for row in file:
            if row['name'] and row['id'] and row['capacity'] and row['room_type'] is not None:
                if Room.objects.filter(id=row['id']).exists() is False:
                    room = Room(id=row['id'],
                                name=row['name'],
                                capacity=row['capacity'],
                                room_type=row['room_type'])
                else:
                    room = Room.objects.filter(id=row['id']).first()
                    room.name = row['name']
                    room.capacity = row['capacity']
                    room.room_type = row['room_type']
                room.save()

        return Response(status=status.HTTP_200_OK)


class CourseJSONImportView(APIView):
    serializer_class = CourseSerializer

    def post(self, request):
        file = json.load(request.FILES['files'])
        for row in file:
            if row['name'] and row['points_value'] and row['id'] is not None:
                course = Course.objects.filter(id=row['id']).first()
                if course is not None:
                    course.name = row['name']
                    course.points_value = row['points_value']
                else:
                    course = Course(id=row['id'], name=row['name'], points_value=row['points_value'])

                if row['prerequisites'] is not None:
                    course.prerequisites = row['prerequisites']
                if row['subject_learning_outcomes'] is not None:
                    course.subject_learning_outcomes = row['subject_learning_outcomes']
                if row['purposes'] is not None:
                    course.purposes = row['purposes']
                if row['methods_of_verification_of_learning_outcomes_and_criteria'] is not None:
                    course.methods_of_verification_of_learning_outcomes_and_criteria = row[
                        'methods_of_verification_of_learning_outcomes_and_criteria']
                if row['content_of_the_subject'] is not None:
                    course.content_of_the_subject = row['content_of_the_subject']
                if row['didactic_methods'] is not None:
                    course.didactic_methods = row['didactic_methods']
                if row['literature'] is not None:
                    course.literature = row['literature']
                if row['balance_of_work_of_an_avg_student'] is not None:
                    course.balance_of_work_of_an_avg_student = row['balance_of_work_of_an_avg_student']
                course.save()

        return Response(status=status.HTTP_200_OK)


class CourseInstructorInfosJSONImportView(APIView):
    serializer_class = CourseInstructorInfoSerializer

    def post(self, request):
        file = json.load(request.FILES['files'])
        for row in file:
            if row['id'] is not None:
                courseinstinfo = CourseInstructorInfo.objects.filter(id=row['id']).first()
                if courseinstinfo is not None:
                    courseinstinfo.hours = row['hours']
                    courseinstinfo.course_type = row['course_type']
                    instructor = StaffAccount.objects.filter(pk=row['instructor']).first()
                    if instructor is not None:
                        courseinstinfo.instructor = instructor
                    course = Course.objects.get(pk=row['course'])
                    if course is not None:
                        courseinstinfo.course = course
                    courseinstinfo.save()
                else:
                    if Course.objects.filter(pk=row['course']).exists() and \
                            StaffAccount.objects.filter(pk=row['instructor']).exists() is not False:
                        if row['course_type'] and row['hours'] is not None:
                            courseinstinfo = CourseInstructorInfo(id=row['id'],
                                                                  hours=row['hours'],
                                                                  course_type=row['course_type'],
                                                                  instructor=StaffAccount.objects.get(
                                                                      pk=row['instructor']),
                                                                  course=Course.objects.get(pk=row['course']))
                            courseinstinfo.save()

        return Response(status=status.HTTP_200_OK)


class SemesterJSONImportView(APIView):
    serializer_class = SemesterSerializer

    def post(self, request):
        file = json.load(request.FILES['files'])
        for row in file:
            year = row['year']
            semester_num = row['semester']
            semester_start_date = row['semester_start_date']
            semester_end_date = row['semester_end_date']
            fieldofstudy_id = row['field_of_study']
            id = row['id']
            if id or fieldofstudy_id or year or semester_num or semester_end_date or semester_start_date is not None:
                if FieldOfStudy.objects.filter(id=fieldofstudy_id).exists():
                    fieldofstudy = FieldOfStudy.objects.filter(id=fieldofstudy_id).first()
                    semester = Semester.objects.filter(id=id).first()
                    if semester is None:
                        semester = Semester(
                            id=id,
                            year=year,
                            semester=semester_num,
                            field_of_study=fieldofstudy,
                            semester_start_date=semester_start_date,
                            semester_end_date=semester_end_date
                        )
                    else:
                        semester.year = year
                        semester.semester = semester_num
                        semester.field_of_study = fieldofstudy
                        semester.semester_start_date = semester_start_date
                        semester.semester_end_date = semester_end_date

                    semester.save()

                    students = row['students']
                    for i in students:
                        if Student.objects.filter(id=i).exists():
                            student = Student.objects.get(id=i)
                            semester.students.add(student)
                            semester.save()

                    courses = row['courses']

                    for i in courses:
                        if Course.objects.filter(id=i).exists():
                            course = Course.objects.get(id=i)
                            semester.courses.add(course)
                            semester.save()
        return Response(status=status.HTTP_200_OK)


class FieldGroupJSONImportView(APIView):
    serializer_class = FieldGroupSerializer

    def post(self, request):
        file = json.load(request.FILES['files'])
        for row in file:
            if row['name'] and row['id'] is not None:
                field_group = FieldGroup.objects.filter(id=row['id']).first()
                if field_group is not None:
                    field_group.name = row['name']
                else:
                    field_group = FieldGroup(id=row['id'], name=row['name'])
                field_group.save()
        return Response(status=status.HTTP_200_OK)


class FieldOfStudyJSONImportView(APIView):
    serializer_class = FieldOfStudySerializer

    def post(self, request):
        file = json.load(request.FILES['files'])
        for row in file:
            name = row['name']
            study_type = row['study_type']
            start_date = row['start_date']
            end_date = row['end_date']
            if row['id'] or name or study_type or start_date or end_date is not None:
                field_of_study = FieldOfStudy.objects.filter(id=row['id']).first()
                if field_of_study is not None:
                    field_of_study.id = row['id']
                    field_of_study.name = name
                    field_of_study.study_type = study_type
                    field_of_study.start_date = start_date
                    field_of_study.end_date = end_date
                else:
                    field_of_study = FieldOfStudy(
                        id=row['id'],
                        name=name,
                        study_type=study_type,
                        start_date=start_date,
                        end_date=end_date
                    )
                field_of_study.save()

                field_groups = row['field_groups']
                for i in field_groups:
                    if FieldGroup.objects.filter(id=i).exists():
                        temp = FieldGroup.objects.get(id=i)
                        field_of_study.field_groups.add(temp)
                        field_of_study.save()

        return Response(status=status.HTTP_200_OK)


class ECTSCardJSONImportView(APIView):
    serializer_class = ECTSCardSerializer

    def post(self, request):
        file = json.load(request.FILES['files'])
        for row in file:
            field_of_study_id = row['field_of_study']
            semester_id = row['semester']
            if row['id'] and field_of_study_id and semester_id is not None:
                semester = Semester.objects.filter(pk=semester_id).first()
                field_of_study = FieldOfStudy.objects.filter(pk=field_of_study_id).first()
                if semester or field_of_study is None:
                    ects_card = ECTSCard.objects.filter(id=row['id']).first()
                    if ects_card is not None:
                        ects_card.semester = semester
                        ects_card.field_of_study = field_of_study
                    else:
                        ects_card = ECTSCard(id=row['id'], semester=semester, field_of_study=field_of_study)
                    ects_card.save()

        return Response(status=status.HTTP_200_OK)


class TimeTableJSONImportView(APIView):
    serializer_class = TimeTableSerializer

    def post(self, request):
        file = json.load(request.FILES['files'])
        for row in file:

            time_table_units = row['time_table_units']
            semester_id = row['semester']
            if semester_id and row['id'] and time_table_units is not None:
                if Semester.objects.filter(id=semester_id).exists():
                    semester = Semester.objects.get(id=semester_id)
                    time_table = TimeTable.objects.filter(id=row['id']).first()
                    if time_table is None:
                        time_table = TimeTable(
                            id=row['id'],
                            semester=semester
                        )
                    else:
                        time_table.semester = semester
                    time_table.save()

                    for i in time_table_units:
                        if TimeTableUnit.objects.filter(id=i).exists():
                            temp = TimeTableUnit.objects.get(id=i)
                            time_table.time_table_units.add(temp)
                            time_table.save()

        return Response(status=status.HTTP_200_OK)


class TimeTableUnitJSONImportView(APIView):
    serializer_class = TimeTableUnitSerializer

    def post(self, request):
        file = json.load(request.FILES['files'])
        for row in file:
            if row['course_instructor_info'] and row['start_hour'] and \
                    row['end_hour'] and row['day'] and row['week'] and row['id'] is not None:
                course_instructor_info_id = row['course_instructor_info']
                if Room.objects.filter(id=row['room']).exists() is False:
                    return Response("Room doesnt exists", status=status.HTTP_400_BAD_REQUEST)
                if CourseInstructorInfo.objects.filter(id=course_instructor_info_id).exists():
                    course_inst_info = CourseInstructorInfo.objects.get(id=course_instructor_info_id)
                    room = Room.objects.get(id=row["room"])
                    time_table_unit = TimeTableUnit.objects.filter(id=row['id']).first()
                    if time_table_unit is None:
                        time_table_unit = TimeTableUnit(id=row['id'],
                                                        course_instructor_info=course_inst_info,
                                                        start_hour=row['start_hour'],
                                                        end_hour=row['end_hour'],
                                                        day=row['day'],
                                                        week=row['week'],
                                                        room=room)
                    else:
                        time_table_unit.course_instructor_info = course_inst_info
                        time_table_unit.start_hour = row['start_hour']
                        time_table_unit.end_hour = row['end_hour']
                        time_table_unit.day = row['day']
                        time_table_unit.week = row['week']
                        time_table_unit.room = room

                    time_table_unit.save()
                    field_groups = row['field_groups']
                    for i in field_groups:
                        if FieldGroup.objects.filter(id=i).exists():
                            temp = FieldGroup.objects.get(id=i)
                            time_table_unit.field_groups.add(temp)
                            time_table_unit.save()

        return Response(status=status.HTTP_200_OK)
