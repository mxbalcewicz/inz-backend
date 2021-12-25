from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents.student import StudentDocument
from .documents.room import RoomDocument
from .documents.fieldgroup import FieldGroupDocument
from .documents.fieldofstudy import FieldOfStudyDocument
from .documents.staffaccount import StaffAccountDocument

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


class FieldGroupDocumentSerializer(DocumentSerializer):
    class Meta:
        """Meta options."""

        # Specify the correspondent document class
        document = FieldGroupDocument

        # Serializer fields
        fields = (
            'id',
            'name',
            'study_type',
            'start_date',
            'end_date',
            'field_groups'
        )


class FieldOfStudyDocumentSerializer(DocumentSerializer):
    class Meta:
        """Meta options."""

        # Specify the correspondent document class
        document = FieldOfStudyDocument

        # Serializer fields
        fields = (
            'id',
            'name',
            'study_type',
            'start_date',
            'end_date',
            'field_groups'
        )

class StaffAccountDocumentSerializer(DocumentSerializer):
    class Meta:
        """Meta options."""

        # Specify the correspondent document class
        document = StaffAccountDocument

        # Serializer fields
        fields = (
            'name',
            'surname',
            'institute',
            'job_title',
            'academic_title',
            'account'
        )