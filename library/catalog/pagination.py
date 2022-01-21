from rest_framework.pagination import PageNumberPagination


class SectionsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_size_query_param = 'rows'

    # max_page_size = 100

    # # TODO a queryset to return all values
    # def paginate_queryset(self, queryset, request, view=None):
    #     if request.query_params.get('get_all', False) == 'true':
    #         return None

    #     return super(SectionsSetPagination, self).paginate_queryset(queryset, request, view=view)
