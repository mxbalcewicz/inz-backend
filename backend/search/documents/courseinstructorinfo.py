from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer, token_filter, normalizer
from api.models import CourseInstructorInfo

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
class CourseInstructorInfoDocument(Document):
    """Elasticsearch document."""

    id = fields.IntegerField(attr='id')
    hours = fields.TextField(
        analyzer=edge_ngram_completion,
        fields={'raw': fields.KeywordField(normalizer=lowercase_normalizer)}
    )
    instructor = fields.NestedField(properties={
        'id': fields.TextField(
            analyzer=edge_ngram_completion,
            fields={'raw': fields.KeywordField(normalizer=lowercase_normalizer)},
        ),
        'email': fields.TextField(
            analyzer=edge_ngram_completion,
            fields={'raw': fields.KeywordField(normalizer=lowercase_normalizer)},
        ),
        'name': fields.TextField(
            analyzer=edge_ngram_completion,
            fields={'raw': fields.KeywordField(normalizer=lowercase_normalizer)}
        ),
        'surname': fields.TextField(
            analyzer=edge_ngram_completion,
            fields={'raw': fields.KeywordField(normalizer=lowercase_normalizer)}),
        'institute': fields.TextField(),
        'job_title': fields.TextField(),
        'academic_title': fields.TextField(),
    })
    course_type = fields.TextField(
        analyzer=edge_ngram_completion,
        fields={'raw': fields.KeywordField(normalizer=lowercase_normalizer)}
    )
    course = fields.NestedField(properties={
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

    def prepare_instructor(self, instance):
        return {
                "id": instance.instructor.account.id,
                "email": instance.instructor.account.email,
                "name": instance.instructor.name,
                "surname": instance.instructor.surname,
                "institute": instance.instructor.institute,
                "job_title": instance.instructor.job_title,
                "academic_title": instance.instructor.academic_title
        }

    class Django(object):
        """Inner nested class Django."""

        model = CourseInstructorInfo  # The model associate with this Document
