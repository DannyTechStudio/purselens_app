from rest_framework.views import APIView
from rest_framework import permissions

from .services import AnalyticsService
from .serializers import (
    AnalyticsOutputSerializer,
    MonthlySummaryItemSerializer,
    CategoryBreakdownSerializer,
    CashflowSerializer,
    BudgetOverviewFieldsSerializer,
    BudgetPerformanceSerializer,
)
from utils.response_helper_methods import success_response

# Create your views here.
class DashboardAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        data = AnalyticsService.get_user_analytics_data(request.user)
        
        serializer = AnalyticsOutputSerializer(instance=data)
        
        return success_response(
            message= "Analytical data retrieved successfully.",
            data=serializer.data
        )
        
class MonthlySummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = AnalyticsService.get_monthly_summary(request.user)
        
        serializer = MonthlySummaryItemSerializer(instance=data, many=True)
        
        return success_response(
            message="Your monthly summaries retrieved successfully.",
            data=serializer.data
        )

class CategoryBreakdownView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = AnalyticsService.get_category_breakdown(request.user)
        
        serializer = CategoryBreakdownSerializer(instance=data, many=True)

        return success_response(
            message="Your category break down retrieved successfully.",
            data=serializer.data
        )

class BudgetPerformanceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = AnalyticsService.get_budget_performance(request.user)
        
        serializer = BudgetPerformanceSerializer(instance=data, many=True)
        
        return success_response(
            message="Your budgets performance retrieved successfully.",
            data=serializer.data
        )

class CashflowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = AnalyticsService.get_cashflow(request.user)
        
        serializer = CashflowSerializer(instance=data, many=True)
        
        return success_response(
            message="Your cashflow retrieved successfully.",
            data=serializer.data
        )
