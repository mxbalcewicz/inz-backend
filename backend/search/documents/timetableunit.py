from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer
from api.models import TimeTableUnit

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


@INDEX.doc_type
class TimeTableUnitDocument(Document):
    """Elasticsearch document."""

    id = fields.IntegerField(attr='id')
    day = fields.TextField()
    week = fields.TextField()
    start_hour = fields.DateField()
    end_hour = fields.DateField()
    course_instructor_info = fields.NestedField(properties={
        'id': fields.IntegerField(attr='id'),
        'hours': fields.IntegerField(),
        'instructor': fields.NestedField(properties={
            'account': fields.NestedField(properties={
                'id': fields.IntegerField(attr='id'),
                'email': fields.TextField(),
            }),
            'name': fields.TextField(),
            'surname': fields.TextField(),
            'institute': fields.TextField(),
            'job_title': fields.TextField(),
            'academic_title': fields.TextField(),
        }),
        'course_type': fields.TextField(),
        'course': fields.NestedField(properties={
            'id': fields.IntegerField(attr='id'),
            'name': fields.TextField(),
            'points_value': fields.IntegerField(),
            'prerequisites': fields.TextField(),
            'purposes': fields.TextField(),
            'subject_learning_outcomes': fields.TextField(),
            'methods_of_verification_of_learning_outcomes_and_criteria': fields.TextField(),
            'content_of_the_subject': fields.TextField(),
            'didactic_methods': fields.TextField(),
            'literature': fields.TextField(),
            'balance_of_work_of_an_avg_student': fields.TextField()
        })
    })
    field_groups = fields.NestedField(properties={
        'id': fields.IntegerField(attr='id'),
        'name': fields.TextField()
    })
    room = fields.NestedField(properties={
        'id': fields.IntegerField(attr='id'),
        'name': fields.TextField(),
        'capacity': fields.IntegerField(),
        'room_type': fields.TextField()
    })

    class Django(object):
        """Inner nested class Django."""

        model = TimeTableUnit  # The model associate with this Document