from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer, token_filter, normalizer
from api.models import FieldGroup

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)

# html_strip = analyzer(
#     'html_strip',
#     tokenizer="standard",
#     filter=["standard", "lowercase", "stop", "snowball"],
#     char_filter=["html_strip"]
# )

edge_ngram_completion_filter = token_filter(
    'edge_ngram_completion_filter',
    type="edge_ngram",
    min_gram=3,
    max_gram=6
)

edge_ngram_completion = analyzer(
    "edge_ngram_completion",
    tokenizer="standard",
    filter=["lowercase", edge_ngram_completion_filter],
    char_filter=["html_strip"],
)

lowercase_normalizer = normalizer(
    'lowercase_normalizer',
    filter=['lowercase']
)


@INDEX.doc_type
class FieldGroupDocument(Document):
    """Elasticsearch document."""

    id = fields.IntegerField(attr='id')
    name = fields.TextField(
        analyzer=edge_ngram_completion,
        fields={'raw': fields.KeywordField(normalizer=lowercase_normalizer)}
    )

    class Django(object):
        """Inner nested class Django."""

        model = FieldGroup  # The model associate with this Document
