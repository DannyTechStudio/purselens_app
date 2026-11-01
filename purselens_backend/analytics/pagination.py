from rest_framework.pagination import PageNumberPagination

class BudgetOverviewPagination(PageNumberPagination):
    page_size = 5
    page_query_param = "page"