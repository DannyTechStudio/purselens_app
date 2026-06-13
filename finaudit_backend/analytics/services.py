from django.db.models import Sum
from finances.models import Transaction
from finances.services import TransactionService, BudgetService


class AnalyticsService:
    """
    Handles all calculation, aggregation, and insight logic 
    for user financial overviews.
    """

    @staticmethod
    def get_financial_summary(income_transactions, expense_transactions) -> dict:
        """Calculates total income, total expenses, and current wallet balance."""
        total_income = income_transactions.aggregate(total=Sum("amount"))["total"] or 0
        total_expense = expense_transactions.aggregate(total=Sum("amount"))["total"] or 0
        balance = total_income - total_expense

        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance
        }

    @staticmethod
    def get_top_categories(expense_transactions, limit=5):
        """Fetches the highest spending categories with totals."""
        return (
            expense_transactions
            .values("category__id", "category__name")
            .annotate(total_spent=Sum("amount"))
            .order_by("-total_spent")[:limit]
        )

    @staticmethod
    def get_budget_overview(expense_transactions, budgets) -> dict:
        """Maps transactions against budgets to calculate overall utilization and risk states."""
        # Group expense transactions by category
        expense_map = {}
        for transaction in expense_transactions:
            expense_map[transaction.category.id] = expense_map.get(transaction.category.id, 0) + transaction.amount

        # Group budget by category
        budget_map = {}
        for budget in budgets:
            budget_map[budget.category.id] = budget_map.get(budget.category.id, 0) + budget.budget_amount

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

        return {
            "total_budget_amount": total_budget_amount,
            "total_spent": total_spent,
            "total_remaining": remaining,
            "overall_utilization": utilization_percentage,
            "budgets_on_track": budgets_on_track,
            "budgets_at_risk": budgets_at_risk,
            "budget_exceeded": budgets_exceeded
        }

    @staticmethod
    def generate_insights(summary, budget_overview, top_categories) -> list:
        """Generates dynamic feedback cards based on spending metrics."""
        insights = []
        total_expense = summary["total_expense"]
        balance = summary["balance"]
        
        exceeded = budget_overview["budget_exceeded"]
        at_risk = budget_overview["budgets_at_risk"]
        total_budget = budget_overview["total_budget_amount"]

        # Budget state insights
        if exceeded > 0:
            insights.append(
                {
                    "type": "danger", 
                    "message": f"You have exceeded {exceeded} budget(s)."
                    }
            )
        if at_risk > 0:
            insights.append(
                {
                    "type": "warning", 
                    "message": f"{at_risk} budget(s) is nearing their limit(s)."
                }
            )
        if at_risk == 0 and exceeded == 0 and total_budget > 0:
            insights.append(
                {
                    "type": "success", 
                    "message": "All budgets are currently on track."
                }
            )
        if total_budget == 0:
            insights.append(
                {
                    "type": "info", 
                    "message": "You have not created any budget yet."
                }
            )

        # Savings metric insights
        savings_rate = (balance / total_expense * 100) if total_expense > 0 else 0
        if savings_rate >= 25:
            insights.append(
                {
                    "type": "success", 
                    "message": "Excellent savings rate this month."
                }
            )
        elif savings_rate < 10 and total_expense > 0:
            insights.append(
                {
                    "type": "warning", 
                    "message": "Your savings rate is lower than recommended."
                }
            )

        # Top category trends and dominance insights (Safely using .first() to prevent empty list crashes)
        top_category = top_categories.first()
        if top_category:
            insights.append(
                {
                    "type": "info", 
                    "message": f"{top_category['category__name']} is your highest spending category."
                }
            )
            
            if total_expense > 0:
                percentage = (top_category["total_spent"] / total_expense) * 100
                if percentage >= 40:
                    insights.append(
                        {
                            "type": "warning",
                            "message": f"{top_category['category__name']} accounts for {percentage:.2f}% of your expenses."
                        }
                    )

        return insights[:5]

    @classmethod
    def get_user_analytics_data(cls, user) -> dict:
        """The Master Orchestrator: Combines helper methods into a cohesive response."""
        
        # 1. Gather raw querysets
        income_transactions = Transaction.objects.filter(type="income", user=user)
        expense_transactions = Transaction.objects.filter(type="expense", user=user)
        budgets = BudgetService.get_user_budgets(user)

        # 2. Extract specific calculations via helper methods
        summary = cls.get_financial_summary(income_transactions, expense_transactions)
        top_categories = cls.get_top_categories(expense_transactions, limit=5)
        budget_overview = cls.get_budget_overview(expense_transactions, budgets)
        insights = cls.generate_insights(summary, budget_overview, top_categories)

        # 3. Fetch independent services
        recent_transactions = (
            TransactionService
            .list_user_transactions(user)
            .order_by("-created_at")[:10]
        )

        # 4. Pack into clean output schema
        return {
            "total_income": summary["total_income"],
            "total_expense": summary["total_expense"],
            "balance": summary["balance"],
            "budgets_overview": budget_overview,
            "top_categories": top_categories,
            "recent_transactions": recent_transactions,
            "insights": insights
        }
