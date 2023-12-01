from rest_framework.pagination import PageNumberPagination


class SimpleResultPagination(PageNumberPagination):
    page_size = 12
    page_query_param = 'page'  # offset
    page_size_query_param = 'page_size'  # limit
    max_page_size = 100