from django.shortcuts import render


from django.http import HttpResponse
from elasticsearch_dsl import Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView

from api.serializers import StudentSerializer, RoomSerializer
from api.documents import StudentDocument, RoomDocument


class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
    serializer_class = None
    document_class = None

    def generate_q_expression(self, query):
        """This method should be
        overridden for every other search view,
        returns a Q() expression."""

    def get(self, request, query):
        try:
            q = self.generate_q_expression(query)
            search = self.document_class.search().query(q)
            response = search.execute()

            print(f'Found {response.hits.total.value} hit(s) for query: "{query}"')

            results = self.paginate_queryset(response, request, view=self)
            serializer = self.serializer_class(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return HttpResponse(e, status=500)


class SearchStudents(PaginatedElasticSearchAPIView):
    serializer_class = StudentSerializer
    document_class = StudentDocument

    def generate_q_expression(self, query):
        return Q(
            'multi_match',
            fields=[
                'name',
                'surname',
            ], fuzziness='auto')


class SearchRooms(PaginatedElasticSearchAPIView):
    serializer_class = RoomSerializer
    document_class = RoomDocument

    def generate_q_expression(self, query):
        return Q(
                'multi_match', query=query,
                fields=[
                    'id',
                    'name',
                    'capacity',
                    'room_type',
                ], fuzziness='auto')