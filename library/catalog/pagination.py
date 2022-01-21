from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from core.models import Book, Author, Category, Serie


class CustomPagePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'rows'

    def paginate_queryset(self, queryset, request, view=None):
        """If 'rows' is not in the url parameters, it will return all the data"""
        if 'rows' not in request.query_params:
            self.page_size = queryset.count()  # To return all values
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        first = self.page.start_index()
        last = self.page.end_index()
        count = last - first + 1
        return Response({
            'pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'countItemsOnPage': count,
            'firstItemOnPage': first,
            'lastItemOnPage': last,
            'current': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data})
