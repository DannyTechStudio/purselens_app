from rest_framework import serializers

from finances.models import Transaction

class TopCategorySerializer(serializers.Serializer):
    category__id = serializers.UUIDField()
    category__name = serializers.CharField()
    total_spent = serializers.DecimalField(max_digits=12, decimal_places=2)

class BudgetOverviewFieldsSerializer(serializers.Serializer):
    total_budget_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_spent = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_remaining = serializers.DecimalField(max_digits=12, decimal_places=2)
    overall_utilization = serializers.DecimalField(max_digits=6, decimal_places=2)
    budgets_on_track = serializers.IntegerField(min_value=0)
    budgets_at_risk = serializers.IntegerField(min_value=0)
    budgets_exceeded = serializers.IntegerField(min_value=0)
    period = serializers.JSONField()

class RecentTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "title", "amount", "type", 
            "category", "description", "transaction_date", 
            "is_recurring", "frequency", "next_due_date"
        ]
        
class FinancialOverview(serializers.Serializer):
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expense = serializers.DecimalField(max_digits=12, decimal_places=2)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)

class InsightCardSerializer(serializers.Serializer):
    type = serializers.CharField()
    message = serializers.CharField()
    
class AnalyticsOutputSerializer(serializers.Serializer):
    financial_overview = FinancialOverview()
    budgets_overview = BudgetOverviewFieldsSerializer()
    top_categories = TopCategorySerializer(many=True)
    recent_transactions = RecentTransactionsSerializer(many=True)
    insights = InsightCardSerializer(many=True)

class MonthlySummaryItemSerializer(serializers.Serializer):
    month = serializers.CharField()
    income = serializers.DecimalField(max_digits=12, decimal_places=2)
    expense = serializers.DecimalField(max_digits=12, decimal_places=2)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)

class CategoryBreakdownSerializer(serializers.Serializer):
    category_id = serializers.UUIDField()
    category_name = serializers.CharField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    percentage = serializers.DecimalField(max_digits=6, decimal_places=2)

class CashflowSerializer(serializers.Serializer):
    month = serializers.CharField()
    inflow = serializers.DecimalField(max_digits=12, decimal_places=2)
    outflow = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_flow = serializers.DecimalField(max_digits=12, decimal_places=2)

class BudgetPerformanceSerializer(serializers.Serializer):
    category_id = serializers.UUIDField()
    category_name = serializers.CharField()
    budget_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    period = serializers.JSONField()
    spent = serializers.DecimalField(max_digits=12, decimal_places=2)
    remaining = serializers.DecimalField(max_digits=12, decimal_places=2)
    utilization = serializers.DecimalField(max_digits=6, decimal_places=2)
    status = serializers.CharField()

