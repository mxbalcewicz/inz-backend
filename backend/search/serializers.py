from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents.student import StudentDocument
from .documents.room import RoomDocument

class StudentDocumentSerializer(DocumentSerializer):
    class Meta:
        """Meta options."""

        # Specify the correspondent document class
        document = StudentDocument

        # Serializer fields
        fields = (
            'id',
            'index',
            'email',
            'name',
            'surname'
        )

class RoomDocumentSerializer(DocumentSerializer):
    class Meta:
        """Meta options."""

        # Specify the correspondent document class
        document = RoomDocument

        # Serializer fields
        fields = (
            'id',
            'name',
            'capacity',
            'room_type',
        )