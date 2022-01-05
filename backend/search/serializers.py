from elasticsearch.serializer import Serializer
from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents.student import StudentDocument
from .documents.room import RoomDocument
from .documents.fieldgroup import FieldGroupDocument
from .documents.fieldofstudy import FieldOfStudyDocument
from .documents.staffaccount import StaffAccountDocument
from .documents.deaneryaccount import DeaneryAccountDocument
from .documents.courseinstructorinfo import CourseInstructorInfoDocument
from .documents.semester import SemesterDocument
from .documents.course import CourseDocument
from .documents.ectscard import ECTSCardDocument
from .documents.timetableunit import TimeTableUnitDocument

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
            'id',
            'name',
            'surname',
            'email',
            'institute',
            'job_title',
            'academic_title',
        )


class DeaneryAccountDocumentSerializer(DocumentSerializer):
    class Meta:
        """Meta options."""

        # Specify the correspondent document class
        document = DeaneryAccountDocument

        # Serializer fields
        fields = (
            'id',
            'email'
        )


class CourseInstructorInfoDocumentSerializer(DocumentSerializer):
    class Meta:
        """Meta options."""

        # Specify the correspondent document class
        document = CourseInstructorInfoDocument

        # Serializer fields
        fields = (
            'id',
            'hours',
            'instructor',
            'course_type',
            'course'
        )


class SemesterDocumentSerializer(DocumentSerializer):
    class Meta:
        """Meta options."""

        # Specify the correspondent document class
        document = SemesterDocument

        # Serializer fields
        fields = (
            'id',
            'semester',
            'year',
            'students',
            'field_of_study',
            'courses',
            'semester_start_date',
            'semester_end_date'
        )


class CourseDocumentSerializer(DocumentSerializer):
    class Meta:
        """Meta options."""

        # Specify the correspondent document class
        document = CourseDocument

        # Serializer fields
        fields = (
            'id',
            'name',
            'points_value',
            'prerequisites',
            'purposes',
            'subject_learning_outcomes',
            'methods_of_verification_of_learning_outcomes_and_criteria',
            'content_of_the_subject',
            'didactic_methods',
            'literature',
            'balance_of_work_of_an_avg_student'
        )


class ECTSCardDocumentSerializer(DocumentSerializer):
    class Meta:
        """Meta options."""

        # Specify the correspondent document class
        document = ECTSCardDocument

        # Serializer fields
        fields = (
            'id',
            'courses',
            'field_of_study',
            'semester'
        )


class TimeTableUnitDocumentSerializer(DocumentSerializer):
    class Meta:
        """Meta options."""

        # Specify the correspondent document class
        document = TimeTableUnitDocument

        # Serializer fields
        fields = (
            'id',
            'day',
            'week',
            'start_hour',
            'end_hour',
            'course_instructor_info',
            'field_groups',
            'room'
        )
