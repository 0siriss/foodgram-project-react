from rest_framework.pagination import PageNumberPagination

from backend.api.services import PAGINATION_SIZE


class LimitPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = PAGINATION_SIZE
