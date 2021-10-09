from rest_framework import viewsets
from .models import (Student,
                     StaffAccount,
                     FieldOfStudy,
                     Course,
                     Room,
                     ECTSCard
                     )
from .serializers import (StudentSerializer,
                          StaffAccountSerializer,
                          FieldOfStudySerializer,
                          CourseSerializer,
                          RoomSerializer,
                          ECTSCardSerializer
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


class ECTSCardViewSet(viewsets.ModelViewSet):
    queryset = ECTSCard.objects.all()
    serializer_class = ECTSCardSerializer
