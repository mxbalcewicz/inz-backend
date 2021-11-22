from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, status
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
                          TimeTableSerializer, TimeTableUnitSerializer
                          )


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
        serializer = self.serializer_class(instructor_info_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseInstructorInfoRetrieveUpdateDeleteView(APIView):
    """
    CourseInstructorInfo retrieve, update, delete view
    """
    serializer_class = CourseInstructorInfoSerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        instance = get_object_or_404(CourseInstructorInfo, pk=pk)
        serializer = self.serializer_class(instance)
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
        course = Course(
            points_value=request.data.get('points_value'),
            name=request.data.get('name'))
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
        serializer = self.serializer_class(course_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseRetrieveUpdateDeleteView(APIView):
    """
    Course retrieve, update, delete view
    """
    serializer_class = CourseSerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        instance = get_object_or_404(Course, pk=pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        instance = Course.objects.get(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = Course.objects.get(pk=pk)
        instance.course_instructor_info.clear()
        course_instructor_info_list = request.data.get('course_instructor_info')
        instance.points_value = request.data.get('points_value')
        instance.name = request.data.get('name')

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
        students = request.data.get('students')
        for i in students:
            if Student.objects.filter(id=i).exists():
                student = Student.objects.get(id=i)
                field_of_study.students.add(student)
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
        serializer = self.serializer_class(field_of_study_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FieldOfStudyRetrieveUpdateDeleteView(APIView):
    """
    FieldOfStudy retrieve, update, delete view
    """
    serializer_class = FieldOfStudySerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        instance = get_object_or_404(FieldOfStudy, pk=pk)
        serializer = self.serializer_class(instance)
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
        students = request.data.get('students')
        field_groups = request.data.get('field_groups')
        instance.field_groups.clear()
        instance.students.clear()

        for i in students:
            if Student.objects.filter(id=i).exists():
                student = Student.objects.get(id=i)
                instance.students.add(student)
                instance.save()

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
                field_of_study=fieldofstudy
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
        serializer = self.serializer_class(semester, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SemesterRetrieveUpdateDeleteView(APIView):
    """
    Semester retrieve, update, delete view
    """
    serializer_class = SemesterSerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        instance = get_object_or_404(Semester, pk=pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        instance = Semester.objects.get(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = Semester.objects.get(pk=pk)

        instance.year = request.data.get('year')
        instance.semester = request.data.get('semester')
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
        serializer = self.serializer_class(ectscard, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ECTSCardRetrieveUpdateDeleteView(APIView):
    """
    ECTSCard retrieve, update, delete view
    """
    serializer_class = ECTSCardSerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        instance = get_object_or_404(ECTSCard, pk=pk)
        serializer = self.serializer_class(instance)
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
        if CourseInstructorInfo.objects.filter(id=course_instructor_info_id).exists():
            course_inst_info = CourseInstructorInfo.objects.get(id=course_instructor_info_id)
            time_table_unit = TimeTableUnit(course_instructor_info=course_inst_info,
                                            hour=request.data.get('hour'),
                                            day=request.data.get('day'),
                                            week=request.data.get('week'))
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
        serializer = self.serializer_class(time_table_unit, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TimeTableUnitRetrieveUpdateDeleteView(APIView):
    """
    TimeTableUnit retrieve, update, delete view
    """
    serializer_class = TimeTableUnitSerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        instance = get_object_or_404(TimeTableUnit, pk=pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        instance = TimeTableUnit.objects.get(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        course_inst_info_id = request.data.get('course_instructor_info')
        if TimeTableUnit.objects.filter(id=pk).exists() and CourseInstructorInfo.objects.filter(
                id=course_inst_info_id).exists():
            instance = TimeTableUnit.objects.get(pk=pk)
            course_inst_info = CourseInstructorInfo.objects.get(id=course_inst_info_id)
            instance.course_instructor_info = course_inst_info
            instance.hours = request.data.get('hours')
            instance.day = request.data.get('day')
            instance.week = request.data.get('week')
            instance.field_groups.clear()
            instance.save()
            field_groups = request.data.get('field_groups')

            for i in field_groups:
                if FieldGroup.object.filter(id=i).exists():
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
        serializer = self.serializer_class(time_table, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TimeTableRetrieveUpdateDeleteView(APIView):
    """
    TimeTable retrieve, update, delete view
    """
    serializer_class = TimeTableSerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        instance = get_object_or_404(TimeTable, pk=pk)
        serializer = self.serializer_class(instance)
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
