from rest_framework import viewsets, status
from .models import Student
from .serializers import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Student records.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
