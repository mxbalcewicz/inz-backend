from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer, normalizer, token_filter
from api.models import Semester

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
class SemesterDocument(Document):
    """Elasticsearch document."""

    id = fields.IntegerField(attr='id')
    semester = fields.TextField()
    year = fields.TextField()
    students = fields.NestedField(properties={
        'id': fields.IntegerField(attr='id'),
        'index': fields.IntegerField(),
        'email': fields.TextField(),
        'name': fields.TextField(
            analyzer=edge_ngram_completion,
            fields={'raw': fields.KeywordField(normalizer=lowercase_normalizer)}
        ),
        'surname': fields.TextField(
            analyzer=edge_ngram_completion,
            fields={'raw': fields.KeywordField(normalizer=lowercase_normalizer)}
        ),
    })
    field_of_study = fields.NestedField(properties={
        'id': fields.IntegerField(attr='id'),
        'name': fields.TextField(
            analyzer=edge_ngram_completion,
            fields={'raw': fields.KeywordField(normalizer=lowercase_normalizer)}
        ),
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
        'name': fields.TextField(
            analyzer=edge_ngram_completion,
            fields={'raw': fields.KeywordField(normalizer=lowercase_normalizer)}
        ),
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

    def prepare_year(self, instance):
        return str(instance.year)

    def prepare_semester(self, instance):
        return str(instance.semester)

    class Django(object):
        """Inner nested class Django."""

        model = Semester  # The model associate with this Document
