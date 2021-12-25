from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer
from api.models import FieldOfStudy

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

@INDEX.doc_type
class FieldOfStudyDocument(Document):
    """Elasticsearch document."""

    id = fields.IntegerField(attr='id')
    name = fields.TextField()
    study_type = fields.TextField()
    start_date = fields.DateField()
    field_groups = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField()
    })

    class Django(object):
        """Inner nested class Django."""

        model = FieldOfStudy  # The model associate with this Document