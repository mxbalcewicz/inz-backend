from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer
from api.models import Student

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
class StudentDocument(Document):
    """Book Elasticsearch document."""

    id = fields.IntegerField(attr='id')
    index = fields.IntegerField()
    email = fields.TextField()
    name = fields.TextField()
    surname = fields.TextField()

    class Django(object):
        """Inner nested class Django."""

        model = Student  # The model associate with this Document