from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer, normalizer, token_filter
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
class CourseDocument(Document):
    """Elasticsearch document."""
    name = fields.TextField(
        analyzer=edge_ngram_completion,
        fields={'raw': fields.KeywordField(normalizer=lowercase_normalizer)}
    )
    points_value = fields.TextField(
        analyzer=edge_ngram_completion,
        fields={'raw': fields.KeywordField(normalizer=lowercase_normalizer)}
    )
    prerequisites = fields.TextField(
        analyzer=edge_ngram_completion,
        fields={'raw': fields.KeywordField(normalizer=lowercase_normalizer)}
    )
    purposes = fields.TextField(
        analyzer=edge_ngram_completion,
        fields={'raw': fields.KeywordField(normalizer=lowercase_normalizer)}
    )
    subject_learning_outcomes = fields.TextField(
        analyzer=edge_ngram_completion,
        fields={'raw': fields.KeywordField(normalizer=lowercase_normalizer)}
    )
    methods_of_verification_of_learning_outcomes_and_criteria = fields.TextField(
        analyzer=edge_ngram_completion,
        fields={'raw': fields.KeywordField(normalizer=lowercase_normalizer)}
    )
    content_of_the_subject = fields.TextField(
        analyzer=edge_ngram_completion,
        fields={'raw': fields.KeywordField(normalizer=lowercase_normalizer)}
    )
    didactic_methods = fields.TextField(
        analyzer=edge_ngram_completion,
        fields={'raw': fields.KeywordField(normalizer=lowercase_normalizer)}
    )
    literature = fields.TextField(
        analyzer=edge_ngram_completion,
        fields={'raw': fields.KeywordField(normalizer=lowercase_normalizer)}
    )
    balance_of_work_of_an_avg_student = fields.TextField(
        analyzer=edge_ngram_completion,
        fields={'raw': fields.KeywordField(normalizer=lowercase_normalizer)}
    )

    def prepare_points_value(self, instance):
        return str(instance.points_value)

    class Django(object):
        """Inner nested class Django."""

        model = Course  # The model associate with this Document
