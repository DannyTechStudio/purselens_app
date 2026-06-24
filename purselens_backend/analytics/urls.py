from django.urls import path
from .views import (
    DashboardAnalyticsView,
    MonthlySummaryView,
    CategoryBreakdownView,
    BudgetPerformanceView,
    CashflowView,
)

urlpatterns = [
    path('dashboard/', DashboardAnalyticsView.as_view(), name='dashboard'),
    path('monthly-summary/', MonthlySummaryView.as_view(), name='monthly-summary'),
    path('category-breakdown/', CategoryBreakdownView.as_view(), name='category-breakdown'),
    path('budget-performance/', BudgetPerformanceView.as_view(), name='budget-performance'),
    path('cashflow/', CashflowView.as_view(), name='cashflow'),
]
