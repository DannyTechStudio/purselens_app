from django.urls import path
from .views import (
    CategoryDetailView,
    CategoryListCreateView,
    TransactionDetailView,
    TransactionListCreateView,
    BudgetDetailView,
    BudgetListCreateView,
)


# API endpoint routes
urlpatterns = [
    path("categories/", CategoryListCreateView.as_view(), name="categories"),
    path("categories/<uuid:category_id>/", CategoryDetailView.as_view(), name="categories-detail"),
    path("transactions/", TransactionListCreateView.as_view(), name="transaction"),
    path("transactions/<uuid:transaction_id>/", TransactionDetailView.as_view(), name="transaction-detail"),
    path("budgets/", BudgetListCreateView.as_view(), name="budgets"),
    path("budgets/<uuid:budget_id>/", BudgetDetailView.as_view(), name="budget-detail"),
]


