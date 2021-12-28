from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer
from api.models import Course

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
class CourseDocument(Document):
    """Elasticsearch document."""
    name = fields.TextField()
    points_value = fields.IntegerField()
    prerequisites = fields.TextField()
    purposes = fields.TextField()
    subject_learning_outcomes = fields.TextField()
    methods_of_verification_of_learning_outcomes_and_criteria = fields.TextField()
    content_of_the_subject = fields.TextField()
    didactic_methods = fields.TextField()
    literature = fields.TextField()
    balance_of_work_of_an_avg_student = fields.TextField()

    class Django(object):
        """Inner nested class Django."""

        model = Course  # The model associate with this Document
