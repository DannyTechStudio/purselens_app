from collections import defaultdict
from django.db.models import Sum
from decimal import Decimal
from django.utils import timezone
from calendar import month_abbr

from finances.models import Transaction
from finances.services import TransactionService, BudgetService


class AnalyticsService:
    """
        Handles all calculation, aggregation, and insight logic 
        for user financial overviews.
    """
    @staticmethod
    def _get_income_transactions(user):
        return Transaction.objects.filter(
            user=user,
            type="income",
            is_active=True
        )

    @staticmethod
    def _get_expense_transactions(user):
        return Transaction.objects.filter(
            user=user,
            type="expense",
            is_active=True
        )
        
    @staticmethod
    def _get_current_period_income(user):
        now = timezone.now()
        
        return Transaction.objects.filter(
            user=user,
            type="income",
            is_active=True,
            transaction_date__year=now.year,
            transaction_date__month=now.month,
        )
        
    @staticmethod
    def _get_current_period_expenses(user):
        now = timezone.now()
        
        return Transaction.objects.filter(
            user=user,
            type="expense",
            is_active=True,
            transaction_date__year=now.year,
            transaction_date__month=now.month,
        )
    
    @staticmethod
    def _build_expense_map(expense_transactions):
        expense_map = defaultdict(Decimal)
        
        for transaction in expense_transactions:
            category_id = transaction.category.id
            
            expense_map[category_id] = (
                expense_map.get(category_id, Decimal("0")) + transaction.amount
            )
            
        return expense_map
    
    @staticmethod
    def _build_budget_map(budgets):
        budget_map = defaultdict(Decimal)

        for budget in budgets:
            category_id = budget.category.id

            budget_map[category_id] = budget.budget_amount

        return budget_map

    @staticmethod
    def get_financial_summary(income_transactions, expense_transactions) -> dict:
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
        """
            Fetches the highest spending categories with totals.
        """
        return (
            expense_transactions
            .values("category__id", "category__name")
            .annotate(total_spent=Sum("amount"))
            .order_by("-total_spent")[:limit]
        )
        
    @staticmethod
    def _get_budget_status(spent, budget_amount):
        threshold = Decimal("0.8")
        
        if spent > budget_amount:
            return "exceeded"
        
        if spent >= budget_amount * threshold:
            return "at_risk"
        
        return "on_track"

    @classmethod
    def get_budget_overview(cls, expense_transactions, budgets):
        """
            Maps transactions against budgets to calculate 
            overall utilization and risk states.
        """
        expense_map = cls._build_expense_map(expense_transactions)
        budget_map = cls._build_budget_map(budgets)
        
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
            spent = expense_map.get(category_id, Decimal("0"))
            status = cls._get_budget_status(spent, budget_amount)
            
            if status == "exceeded":
                budgets_exceeded += 1
            elif status == "at_risk":
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
            "budgets_exceeded": budgets_exceeded
        }

    @staticmethod
    def generate_insights(summary, budget_overview, top_categories) -> list:
        """
            Generates dynamic feedback cards based on spending metrics.
        """
        insights = []
        total_expense = summary["total_expense"]
        balance = summary["balance"]
        
        exceeded = budget_overview["budgets_exceeded"]
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

        # Top category trends and dominance insights
        top_categories = list(top_categories)
        top_category = (
            top_categories[0]
            if top_categories else None
        )
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
        """
            The Master Orchestrator: Combines helper methods into a 
            cohesive response.
        """
        
        # Gather raw querysets
        income_transactions = cls._get_current_period_income(user)
        expense_transactions = cls._get_current_period_expenses(user)
        budgets = BudgetService.get_user_budgets(user)

        # Extract specific calculations using helper methods
        summary = cls.get_financial_summary(income_transactions, expense_transactions)
        top_categories = list(cls.get_top_categories(expense_transactions, limit=5))
        budget_overview = cls.get_budget_overview(expense_transactions, budgets)
        insights = cls.generate_insights(summary, budget_overview, top_categories)

        # Fetch independent services
        recent_transactions = (
            TransactionService
            .list_user_transactions(user)
            .order_by("-created_at")[:10]
        )

        # Pack into clean output schema
        return {
            "total_income": summary["total_income"],
            "total_expense": summary["total_expense"],
            "balance": summary["balance"],
            "budgets_overview": budget_overview,
            "top_categories": top_categories,
            "recent_transactions": recent_transactions,
            "insights": insights
        }

    @classmethod
    def get_monthly_summary(cls, user):
        transactions = Transaction.objects.filter(
            user=user,
            is_active=True
        )
       
        monthly_data = defaultdict(
            lambda: {
                "income": 0,
                "expense": 0
            }
        )
       
        for transaction in transactions:
            month_number = transaction.transaction_date.month

            if transaction.type == "income":
                monthly_data[month_number]["income"] += transaction.amount
            else:
                monthly_data[month_number]["expense"] += transaction.amount
                
        results = []
        
        for month_number in sorted(monthly_data.keys()):
            income = monthly_data[month_number]["income"]
            expense = monthly_data[month_number]["expense"]
            
            results.append(
                {
                    "month": month_abbr[month_number],
                    "income": income,
                    "expense": expense,
                    "balance": income - expense
                }
            )
            
        return results
           
    @classmethod
    def get_category_breakdown(cls, user):
        expense_transactions = cls._get_expense_transactions(user)
        total_expense = (
            expense_transactions.aggregate(
                total=Sum("amount")
            )["total"] or 0
        )
        
        categories = (expense_transactions
            .values(
                "category__id",
                "category__name"
            )
            .annotate(
                amount=Sum("amount")
            )
            .order_by("-amount")
        )
        
        results = []
        for category in categories:
            percentage = (
                (category["amount"] / total_expense) * 100
                if total_expense > 0 else 0
            )
            
            results.append(
                {
                    "category_id": category["category__id"],
                    "category_name": category["category__name"],
                    "amount": category["amount"],
                    "percentage": round(percentage, 2)
                }
            )
            
        return results
    
    @classmethod
    def get_budget_performance(cls, user):
        budgets = BudgetService.get_user_budgets(user)
        expense_transactions = cls._get_current_period_expenses(user)
        expense_map = cls._build_expense_map(expense_transactions)
        
        results = []
        for budget in budgets:
            spent = expense_map.get(budget.category.id, 0)
            remaining = (budget.budget_amount - spent)
            utilization = (
                (spent / budget.budget_amount) * 100
                if budget.budget_amount > 0 else 0
            )
            
            status = cls._get_budget_status(spent, budget.budget_amount)
                
            results.append(
                {
                    "category_id": budget.category.id,
                    "category_name": budget.category.name,
                    "budget_amount": budget.budget_amount,
                    "period": {
                        "start_date": budget.start_date,
                        "end_date": budget.end_date,
                    },
                    "spent": spent,
                    "remaining": remaining,
                    "utilization": round(utilization, 2),
                    "status": status
                }
            )
            
        return results
            
    @classmethod
    def get_cashflow(cls, user):
        monthly_summary = cls.get_monthly_summary(user)
        
        return [
            {
                "month": item["month"],
                "inflow": item["income"],
                "outflow": item["expense"],
                "net_flow": item["balance"]
            }
            for item in monthly_summary
        ]
    
           