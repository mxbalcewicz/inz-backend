from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView

from .models import (Student,
                     StaffAccount,
                     FieldOfStudy,
                     Course,
                     Room,
                     ECTSCard,
                     Student,
                     CourseInstructorInfo,
                     Semester
                     )
from .serializers import (StudentSerializer,
                          StaffAccountSerializer,
                          FieldOfStudySerializer,
                          CourseSerializer,
                          RoomSerializer,
                          ECTSCardSerializer,
                          CourseInstructorInfoSerializer,
                          SemesterSerializer
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
        instructor_id = request.data.get('instructor')
        if StaffAccount.objects.filter(pk=instructor_id).exists():
            instructor_instance = StaffAccount.objects.get(pk=instructor_id)
            courseInstructorInfo = CourseInstructorInfo(
                hours=request.data.get('hours'),
                instructor=instructor_instance,
                course_type=request.data.get('course_type')
            )
            courseInstructorInfo.save()

            # serializer.accounts.StaffAccount = instructor_id
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        deanery_accounts = CourseInstructorInfo.objects.all()
        serializer = self.serializer_class(deanery_accounts, many=True)
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
        courseinstrinfo_id = request.data.get('course_instructor_info')
        if CourseInstructorInfo.objects.filter(pk=courseinstrinfo_id).exists():
            courseinstrinfo_instance = CourseInstructorInfo.objects.get(pk=courseinstrinfo_id)
            course = Course(
                points_value=request.data.get('points_value'),
                name=request.data.get('name')
            )
            course.course_instructor_info = courseinstrinfo_instance
            course.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        deanery_accounts = Course.objects.all()
        serializer = self.serializer_class(deanery_accounts, many=True)
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

    # NEEDS TO BE FIXED
    def put(self, request, pk):
        instance = Course.objects.get(pk=pk)
        courseinstinfo_id = request.data.get('course_instructor_info')
        if CourseInstructorInfo.objects.filter(pk=courseinstinfo_id).exists():
            courseinstinfo_instance = CourseInstructorInfo.objects.get(pk=courseinstinfo_id)
            instance.course_instructor_info = courseinstinfo_instance
            instance.points_value = request.data.get('points_value')
            instance.name = request.data.get('name')
            instance.save()
            updated_instance = CourseInstructorInfo.objects.get(pk=pk)
            serializer = self.serializer_class(updated_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


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

            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        fieldOfStudy = FieldOfStudy.objects.all()
        serializer = self.serializer_class(fieldOfStudy, many=True)
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
        instance.save()

        students = request.data.get('students')
        for i in students:
            if Student.objects.filter(id=i).exists():
                student = Student.objects.get(id=i)
                instance.students.add(student)
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

        instance.save()
        students = request.data.get('students')
        for i in students:
            if Student.objects.filter(id=i).exists():
                student = Student.objects.get(id=i)
                instance.students.add(student)
                instance.save()

        courses = request.data.get('courses')
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
        fieldofstudy_id = request.data.get('field_of_study')
        semester_id = request.data.get('semester')
        if FieldOfStudy.objects.filter(id=fieldofstudy_id).exists() and Semester.objects.filter(
                id=semester_id).exists():
            fieldofstudy = FieldOfStudy.objects.get(id=fieldofstudy_id)
            semester = Semester.objects.get(id=semester_id)
            ectscard = ECTSCard(
                semester=semester,
                field_of_study=fieldofstudy
            )
            ectscard.save()

            courses = request.data.get('courses')
            for i in courses:
                if Course.objects.filter(id=i).exists():
                    course = Course.objects.get(id=i)
                    ectscard.courses.add(course)
                    ectscard.save()
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
            instance.field_of_study=fieldofstudy
            instance.semester=semester
            instance.save()

            courses = request.data.get('courses')
            for i in courses:
                if Course.objects.filter(id=i).exists():
                    course = Course.objects.get(id=i)
                    instance.courses.add(course)
                    instance.save()

            courses = request.data.get('courses')
            for i in courses:
                if Course.objects.filter(id=i).exists():
                    course = Course.objects.get(id=i)
                    instance.courses.add(course)
                    instance.save()

            updated_instance = ECTSCard.objects.get(pk=pk)
            serializer = self.serializer_class(updated_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
