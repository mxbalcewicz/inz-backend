from django_elasticsearch_dsl import indices
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
    MultiMatchSearchFilterBackend,
    CompoundSearchFilterBackend
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from elasticsearch import Elasticsearch as es, serializer
from elasticsearch_dsl import Search, Q
import json
from .documents.student import StudentDocument
from .documents.room import RoomDocument
from .documents.fieldgroup import FieldGroupDocument
from .documents.fieldofstudy import FieldOfStudyDocument
from .documents.staffaccount import StaffAccountDocument
from .documents.deaneryaccount import DeaneryAccountDocument
from .documents.courseinstructorinfo import CourseInstructorInfoDocument
from .documents.semester import SemesterDocument
from .documents.ectscard import ECTSCardDocument
from .documents.course import CourseDocument
from elasticsearch_dsl import connections
from elasticsearch_dsl.query import MultiMatch, Match
from .serializers import (
    ECTSCardDocumentSerializer,
    FieldGroupDocumentSerializer,
    StudentDocumentSerializer,
    RoomDocumentSerializer,
    FieldOfStudyDocumentSerializer,
    StaffAccountDocumentSerializer,
    DeaneryAccountDocumentSerializer,
    CourseInstructorInfoDocumentSerializer,
    SemesterDocumentSerializer,
    CourseDocumentSerializer
)

class SearchAllDocumentsView(APIView):

    def get(self, request, query):
        q = Q("multi_match", query=query, fields="*")                                                                                                                                    
        con = connections.get_connection()
        s = Search().using(con).query(q)
        response = s.execute().to_dict()

        res_data = response["hits"]["hits"]
        index_values = set()
        for item in res_data:
            index_values.add(item['_index'])
        print(index_values)
        
        results_list = []

        for index in index_values:
            results = [item['_source'] for item in res_data if item['_index'] == index]
            data = {
                "type": index,
                "results": results
            }
            results_list.append(data)
            
        print(results_list)

        return Response(data=results_list, status=status.HTTP_200_OK)

class StudentDocumentView(DocumentViewSet):
    document = StudentDocument
    serializer_class = StudentDocumentSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        CompoundSearchFilterBackend,
        DefaultOrderingFilterBackend,
    ]
    # Define search fields
    search_fields = (
        'email',
        'name',
        'surname',
        'index'
    )
    # Define filter fields
    filter_fields = {
        'id': 'id'
    }
    # Define ordering fields
    ordering_fields = {
        'id': 'id',
    }

    ordering = ('id')


class RoomDocumentView(DocumentViewSet):
    document = RoomDocument
    serializer_class = RoomDocumentSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]
    # Define search fields
    search_fields = (
        'name',
        'room_type'
    )
    # Define filter fields
    filter_fields = {
        'id': 'id',
        'name': 'name',
        'room_type': 'room_type',
        'capacity': 'capacity'
    }
    # Define ordering fields
    ordering_fields = {
        'id': 'id',
        'capacity': 'capacity'
    }

    ordering = ('id', 'capacity')


class FieldGroupDocumentView(DocumentViewSet):
    document = FieldGroupDocument
    serializer_class = FieldGroupDocumentSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]
    # Define search fields
    search_fields = (
        'name',
    )
    # Define filter fields
    filter_fields = {
        'id': 'id',
        'name': 'name'
    }
    # Define ordering fields
    ordering_fields = {
        'id': 'id',
    }

    ordering = ('id')


class FieldOfStudyDocumentView(DocumentViewSet):
    document = FieldOfStudyDocument
    serializer_class = FieldOfStudyDocumentSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]
    # Define search fields
    search_fields = (
        'name',
        'study_type',
    )

    search_nested_fields = {
        'field_groups': {
        'path': 'field_groups',
        'fields': ['name']
        }
    }
    # Define filter fields
    filter_fields = {
        'id': 'id',
        'study_type': 'study_type',
    }
    # Define ordering fields
    ordering_fields = {
        'id': 'id',
    }

    ordering = ('id')


class StaffAccountDocumentView(DocumentViewSet):
    document = StaffAccountDocument
    serializer_class = StaffAccountDocumentSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        CompoundSearchFilterBackend,
        DefaultOrderingFilterBackend,
    ]
    # Define search fields
    search_fields = (
        'name',
        'surname',
        'email',
        'academic_title',
        'job_title',
        'institute'
    )
    # Define filter fields
    filter_fields = {
        'id': 'id',
        'name': 'name',
        'surname': 'surname',
        'email': 'email',
        'academic_title': 'academic_title',
        'job_title': 'job_title',
        'institute': 'institute'
    }

    ordering_fields = {
        'id': 'id',
    }


class DeaneryAccountDocumentView(DocumentViewSet):
    document = DeaneryAccountDocument
    serializer_class = DeaneryAccountDocumentSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]
    # Define search fields
    search_fields = (
        'email',
    )
    # Define filter fields
    filter_fields = {
        'id': 'id'
    }

    ordering_fields = {
        'id': 'id'
    }


class CourseInstructorInfoDocumentView(DocumentViewSet):
    document = CourseInstructorInfoDocument
    serializer_class = CourseInstructorInfoDocumentSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]
    # Define search fields
    search_fields = (
        'hours',
        'course_type',
    )

    search_nested_fields = {
        'instructor': {
        'path': 'instructor',
        'fields': ['name', 'surname']
        },
        'course': {
            'path': 'course',
            'fields': ['name']
        }
    }
    # Define filter fields
    filter_fields = {
        'id': 'id'
    }

    ordering_fields = {
        'id': 'id'
    }


class SemesterDocumentView(DocumentViewSet):
    document = SemesterDocument
    serializer_class = SemesterDocumentSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]
    # Define search fields
    search_fields = (
        'semester',
        'year',
    )

    search_nested_fields = {
        'students': {
        'path': 'students',
        'fields': ['name', 'surname']
        },
        'field_of_study': {
            'path': 'field_of_study',
            'fields': ['name']
        },
        'courses': {
            'path': 'courses',
            'fields': ['name']
        },
    }

    # Define filter fields
    filter_fields = {
        'id': 'id',
        'semester': 'semester',
        'year': 'year'
    }

    ordering_fields = {
        'id': 'id'
    }


class CourseDocumentView(DocumentViewSet):
    document = CourseDocument
    serializer_class = CourseDocumentSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]
    # Define search fields
    search_fields = (
        'name',
        'points_value',
        'prerequisites',
        'purposes',
        'subject_learning_outcomes',
        'methods_of_verification_of_learning_outcomes_and_criteria',
        'content_of_the_subject',
        'didactic_methods',
        'literature',
        'balance_of_work_of_an_avg_student',
    )
    # Define filter fields
    filter_fields = {
        'id': 'id',
        'name': 'name',
        'points_value': 'points_value',
        'prerequisites': 'prerequisites',
        'purposes': 'purposes',
        'subject_learning_outcomes': 'subject_learning_outcomes',
        'methods_of_verification_of_learning_outcomes_and_criteria': 'methods_of_verification_of_learning_outcomes_and_criteria',
        'content_of_the_subject': 'content_of_the_subject',
        'didactic_methods': 'didactic_methods',
        'literature': 'literature',
        'balance_of_work_of_an_avg_student': 'balance_of_work_of_an_avg_student'
    }

    ordering_fields = {
        'id': 'id'
    }


class ECTSCardDocumentView(DocumentViewSet):
    document = ECTSCardDocument
    serializer_class = ECTSCardDocumentSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]
    # Define search fields
    search_fields = (
        'id'
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

    ordering_fields = {
        'id': 'id'
    }
