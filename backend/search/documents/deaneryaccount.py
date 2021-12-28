from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer
from accounts.models import DeaneryAccount

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
class DeaneryAccountDocument(Document):
    """Book Elasticsearch document."""

    account = fields.NestedField(properties={
        'id': fields.IntegerField(attr='id'),
        'email': fields.TextField()
    })

    class Django(object):
        """Inner nested class Django."""

        model = DeaneryAccount  # The model associate with this Document
