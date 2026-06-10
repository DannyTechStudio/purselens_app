from rest_framework import serializers

from .models import (
    Category, 
    CategoryTypeEnum, 
    Transaction, 
    TransactionFrequencyEnum,
    TransactionTypeEnum,
    Budget,
    BudgetPeriodEnum,
)


# Create your serializers here.
"""
    Category Serializers
"""
class CategoryCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    type = serializers.ChoiceField(choices=CategoryTypeEnum.choices)
    
class CategoryUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50, required=False)
    type = serializers.ChoiceField(choices=CategoryTypeEnum.choices, required=False)
    is_active = serializers.BooleanField(required=False) 

class CategoryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


"""
    Transaction Serializers
"""
class TransactionCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    type = serializers.ChoiceField(choices=TransactionTypeEnum.choices)
    category_id = serializers.UUIDField()
    description = serializers.CharField(max_length=1000, required=False, allow_blank=True)
    transaction_date = serializers.DateField()
    is_recurring = serializers.BooleanField(default=False)
    frequency = serializers.ChoiceField(
        choices=TransactionFrequencyEnum.choices,
        required=False
    )
    next_due_date = serializers.DateField(required=False)
    
class TransactionUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50, required=False)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    category_id = serializers.UUIDField(required=False)
    type = serializers.ChoiceField(choices=TransactionTypeEnum.choices, required=False)

    description = serializers.CharField(max_length=1000, required=False, allow_blank=True)
    transaction_date = serializers.DateField(required=False)

    is_recurring = serializers.BooleanField(required=False)
    frequency = serializers.ChoiceField(
        choices=TransactionFrequencyEnum.choices,
        required=False
    )
    next_due_date = serializers.DateField(required=False)
        
class TransactionResponseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    
    class Meta:
        model = Transaction
        fields = "__all__"



"""
    Budget Serializers
"""
class BudgetCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)
    category_id = serializers.UUIDField()
    budget_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    period_type = serializers.ChoiceField(choices=BudgetPeriodEnum.choices)
    start_date = serializers.DateField()
    end_date = serializers.DateField()

class BudgetUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50, required=False)
    category_id = serializers.UUIDField(required=False)
    budget_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    period_type = serializers.ChoiceField(choices=BudgetPeriodEnum.choices, required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)

class BudgetResponseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    
    class Meta:
        model = Budget
        fields = "__all__"

