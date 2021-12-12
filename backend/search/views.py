from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    LOOKUP_QUERY_EXCLUDE,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination

from .documents.student import StudentDocument
from .serializers import StudentDocumentSerializer


class StudentDocumentView(BaseDocumentViewSet):

    document = StudentDocument
    serializer_class = StudentDocumentSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    # filter_backends = [
    #     FilteringFilterBackend,
    #     IdsFilterBackend,
    #     OrderingFilterBackend,
    #     DefaultOrderingFilterBackend,
    #     SearchFilterBackend,
    # ]
    # Define search fields
    search_fields = (
        'email',
        'name',
        'surname',
    )
    # Define filter fields
    filter_fields = {
        'id': {
            'field': 'id',
            # Note, that we limit the lookups of id field in this example,
            # to `range`, `in`, `gt`, `gte`, `lt` and `lte` filters.
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
    }
    # Define ordering fields
    ordering_fields = {
        'id': 'id',
        'index': 'index',
    }