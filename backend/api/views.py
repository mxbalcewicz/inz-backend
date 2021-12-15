from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers, viewsets, status
from rest_framework.views import APIView

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
                          TimeTableGetSerializer, CourseInstructorInfoGetSerializer, CourseGetSerializer
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
        if StaffAccount.objects.filter(pk=instructor_id).exists():
            instructor_instance = StaffAccount.objects.get(pk=instructor_id)
            instance.instructor = instructor_instance
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

        course_instructor_info = request.data.get('course_instructor_info')
        course.save()
        for i in course_instructor_info:
            if CourseInstructorInfo.objects.filter(id=i).exists():
                temp = CourseInstructorInfo.objects.get(id=i)
                course.course_instructor_info.add(temp)
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

        if request.data.get('course_instructor_info') is not None:
            course_instructor_info_list = request.data.get('course_instructor_info')
            instance.course_instructor_info.clear()
            for instructor_info_id in course_instructor_info_list:
                info_object = CourseInstructorInfo.objects.get(id=instructor_info_id)
                instance.course_instructor_info.add(info_object)
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

        courses = request.data.get('courses')
        instance.courses.clear()
        for i in courses:
            if Course.objects.filter(id=i).exists():
                course = Course.objects.get(id=i)
                instance.courses.add(course)
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


class StudentsCSVExportView(APIView):
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Students.csv"'

        serializer = self.serializer_class(queryset=Student.objects.all(), many=True)
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

        serializer = self.serializer_class(queryset=CourseInstructorInfo.objects.all(), many=True)
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
            queryset=Room.objects.all(),
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
            queryset=Course.objects.all(),
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
            queryset=Semester.objects.all(),
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
            queryset=FieldGroup.objects.all(),
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
            queryset=ECTSCard.objects.all(),
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
            queryset=TimeTableUnit.objects.all(),
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
            queryset=TimeTable.objects.all(),
            many=True
        )
        header = self.serializer_class.Meta.fields

        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)

        return response
