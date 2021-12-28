from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer
from api.models import Semester

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
class SemesterDocument(Document):
    """Elasticsearch document."""

    id = fields.IntegerField(attr='id')
    semester = fields.IntegerField()
    year = fields.IntegerField()
    students = fields.NestedField(properties={
        'id': fields.IntegerField(attr='id'),
        'index': fields.IntegerField(),
        'email': fields.TextField(),
        'name': fields.TextField(),
        'surname': fields.TextField(),
    })
    field_of_study = fields.NestedField(properties={
        'id': fields.IntegerField(attr='id'),
        'name': fields.TextField(),
        'study_type': fields.TextField(),
        'start_date': fields.DateField(),
        'end_date': fields.DateField(),
        'field_groups': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        })
    })
    courses = fields.NestedField(properties={
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
    semester_start_date = fields.DateField()
    semester_end_date = fields.DateField()

    class Django(object):
        """Inner nested class Django."""

        model = Semester  # The model associate with this Document