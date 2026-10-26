from rest_framework.pagination import PageNumberPagination

class TransactionPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page"


class CategoryPagination(PageNumberPagination):
    page_size = 15
    page_query_param = "page"


class BudgetPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page"