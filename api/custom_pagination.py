from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from collections import OrderedDict

class CustomPagination(PageNumberPagination):

    page_size = 2
    page_query_param = 'page_number'
    page_size_query_param = 'per_page'

    def paginate_queryset(self, queryset, request, view=None):

        try:
            return super().paginate_queryset(queryset, request, view)
        
        except:
            return list(queryset)
    
    def get_paginated_response(self, data, statusCode):

        try:
            return Response(OrderedDict([
            ('total', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data)
                ]
            ), status=statusCode)
        
        except:
            return Response({'statusCode': status.HTTP_404_NOT_FOUND, 'error': self.invalid_page_message, 'data': []})