from django.db.models import Sum
from finances.models import Transaction
from finances.services import TransactionService, BudgetService


def get_user_analytics_data(user) -> dict:
    # Fetch foundations
    income_transactions = Transaction.objects.filter(type="income", user=user)
    expense_transactions = Transaction.objects.filter(type="expense", user=user)
    budgets = BudgetService.get_user_budgets(user)

    # Total income transaction
    total_income = income_transactions.aggregate(
        total=Sum("amount")
    )["total"] or 0
    
    # Total expense transaction
    total_expense = expense_transactions.aggregate(
        total=Sum("amount")
    )["total"] or 0
    
    # Balance
    balance = total_income - total_expense
    
    # Top 5 expense categories
    top_category_totals = (
        expense_transactions
        .values("category__id", "category__name")
        .annotate(total_spent=Sum("amount"))
        .order_by("-total_spent")[:5]
    )
    
    # Group expense transactions by category
    expense_map = {}
    for expense_transaction in expense_transactions:
        category_id = expense_transaction.category.id
        
        expense_map[category_id] = (
            expense_map.get(category_id, 0) + expense_transaction.amount
        )

    # Group budget by category
    budget_map = {}
    for budget in budgets:
        category_id = budget.category.id
        
        budget_map[category_id] = (
            budget_map.get(category_id, 0) + budget.budget_amount 
        )
    
    total_budget_amount = sum(budget_map.values())
    total_spent = sum(expense_map.values())
    remaining = total_budget_amount - total_spent
    
    utilization_percentage = (
        (total_spent / total_budget_amount) * 100
        if total_budget_amount > 0 else 0
    )
    
    budgets_on_track = 0
    budgets_at_risk = 0
    budgets_exceeded = 0
    
    for category_id, budget_amount in budget_map.items():
        spent = expense_map.get(category_id, 0)
        
        if spent > budget_amount:
            budgets_exceeded += 1
        elif spent >= (budget_amount * 0.8):
            budgets_at_risk += 1
        else:
            budgets_on_track += 1
   
    # Recent transactions(10)
    recent_transactions = (
        TransactionService
        .list_user_transactions(user)
        .order_by("-created_at")[:10]
    )
    
    # Accumulate response
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "budgets_overview": {
            "total_budget_amount": total_budget_amount,
            "total_spent": total_spent,
            "total_remaining": remaining,
            "overall_utilization": utilization_percentage,
            "budgets_on_track": budgets_on_track,
            "budgets_at_risk": budgets_at_risk,
            "budget_exceeded": budgets_exceeded
        },
        "top_categories": top_category_totals,
        "recent_transactions": recent_transactions
    }

