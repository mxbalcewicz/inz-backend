from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from api.models import Student, FieldGroup, Room
from accounts.models import DeaneryAccount, StaffAccount


@registry.register_document
class StudentDocument(Document):
    class Index:
        name = 'students'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Student
        fields = [
            'id',
            'index',
            'email',
            'name',
            'surname'
        ]


@registry.register_document
class FieldGroupDocument(Document):
    class Index:
        name = 'fieldgroups'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = FieldGroup
        fields = [
            'id',
            'name'
        ]


class StaffAccountDocument(Document):
    account = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'email': fields.TextField(),
    })

    class Index:
        name = 'staffaccounts'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = StaffAccount
        fields = [
            'name',
            'surname',
            'institute',  # Temp for changes to model institute
            'job_title',
            'academic_title',
        ]


class DeaneryAccountDocument(Document):
    account = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'email': fields.TextField(),
    })

    class Index:
        name = 'deaneryaccounts'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = DeaneryAccount


class RoomDocument(Document):
    class Index:
        name = 'rooms'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Room
        fields = [
            'id',
            'name',
            'capacity',
            'room_type',
        ]