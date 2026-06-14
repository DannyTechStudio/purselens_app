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
    overall_utilization = serializers.DecimalField(max_digits=12, decimal_places=2)
    budgets_on_track = serializers.IntegerField(min=0)
    budget_at_risk = serializers.IntegerField(min=0)
    budget_exceeded = serializers.IntegerField(min=0)
    

class RecentTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "title", "amount", "type", 
            "category", "description", "transaction_date", 
            "is_recurring", "frequency", "next_due_date"
        ]
        

class InsightCardSerializer(serializers.Serializer):
    type = serializers.CharField()
    message = serializers.CharField()
    
class AnalyticsOutputSerializer(serializers.Serializer):
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expense = serializers.DecimalField(max_digits=12, decimal_places=2)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    budgets_overview = BudgetOverviewFieldsSerializer()
    top_categories = TopCategorySerializer(many=True)
    recent_transactions = RecentTransactionsSerializer(many=True)
    insights = InsightCardSerializer(many=True)

