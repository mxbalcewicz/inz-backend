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


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Student records.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StaffUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StaffAccount.objects.all()
    serializer_class = StaffAccountSerializer


class FieldOfStudyViewSet(viewsets.ModelViewSet):
    queryset = FieldOfStudy.objects.all()
    serializer_class = FieldOfStudySerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


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
        deanery_accounts = Room.objects.all()
        serializer = self.serializer_class(deanery_accounts, many=True)
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

