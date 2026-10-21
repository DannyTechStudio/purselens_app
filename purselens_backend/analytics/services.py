from collections import defaultdict
from django.db.models import Q, Sum, Count
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta, date
from calendar import month_abbr, monthrange, month_name, month

from finances.models import Transaction, Budget
from finances.services import CategoryService, TransactionService, BudgetService


class AnalyticsService:
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
    def _get_user_current_budgets(user):
        current_date = timezone.now().date()
        
        month_start_date = current_date.replace(day=1)
        month_end_date = current_date.replace(day=monthrange(current_date.year, current_date.month)[1])
        
        return Budget.objects.filter(
            user=user, 
            is_active=True, 
            start_date__lte=month_end_date, 
            end_date__gte=month_start_date,
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
        total_expense_transactions = expense_transactions.count()
        
        if total_expense_transactions == 0:
            return []
        
        categories = (
            expense_transactions
            .values("category__id", "category__name")
            .annotate(
                total_spent=Sum("amount"),
                transaction_count=Count("id"),
            )
            .order_by("-total_spent")[:limit]
        )
        
        return [
            {
                "category_id": category["category__id"],
                "category_name": category["category__name"],
                "total_spent": category["total_spent"],
                "transaction_count": category["transaction_count"],
                "transaction_percentage": (
                    category["transaction_count"]
                    / total_expense_transactions
                ) * 100,
            }
            for category in categories
        ]
        
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
        if not budgets.exists():
            return {
                "total_budget_amount": Decimal("0"),
                "total_spent": Decimal("0"),
                "total_remaining": Decimal("0"),
                "overall_utilization": 0,
                "budgets_on_track": 0,
                "budgets_at_risk": 0,
                "budgets_exceeded": 0,
                "period": None,
            }
            
        first_budget = budgets.first()
        
        period = {
            "label": first_budget.start_date.strftime("%B %Y"),
            "start_date": first_budget.start_date,
            "end_date": first_budget.end_date,
        }
        
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
            "utilization_percent": utilization_percentage,
            "budgets_on_track": budgets_on_track,
            "budgets_at_risk": budgets_at_risk,
            "budgets_exceeded": budgets_exceeded,
            "period": period,
        }

    @classmethod
    def period_resolver(cls, period):
        period_constants = [
            'all_time',
            'current_month',
            'last_month', 
            'last_3_months_current_month_inclusive',
            'last_3_months_current_month_exclusive',
            'last_6_months_current_month_inclusive',
            'last_6_months_current_month_exclusive',
            'current_year',
            'last_year',
        ]
        
        if period not in period_constants:
            raise ValueError(
                f"Unsupported analytical period: {period}"
            )
        
        # current_date = timezone.now().date()
        current_date = timezone.localdate()
        
        first_day_of_current_month = current_date.replace(day=1)
        
        def get_month_start(months_back):
            month_index = first_day_of_current_month.month - months_back
            year = first_day_of_current_month.year
            
            while month_index <= 0:
                month_index += 12
                year -=1
                
            return first_day_of_current_month.replace(
                year=year,
                month=month_index
            )
        
        if period == "all_time":
            return {
                "period_type": "all_time",
                "start_date": None,
                "end_date": None,
                "label": "All time",
            }
        
        if period == "current_month":
            return {
                "period_type": "current_month",
                "start_date": first_day_of_current_month,
                "end_date": current_date,
                "label": "Current month",
            }
            
        if period == "last_month":
            end_date = first_day_of_current_month - timedelta(days=1)
            start_date = end_date.replace(day=1)
            
            return {
                "period_type": "last_month",
                "start_date": start_date,
                "end_date": end_date,
                "label": "Last month"
            }
            
        if period == "last_3_months_current_month_inclusive":
            return {
                "period_type": period,
                "start_date": get_month_start(2),
                "end_date": current_date,
                "label": "Last 3 months (Current month inclusive)"
            }
        
        if period == "last_3_months_current_month_exclusive":
            end_date = first_day_of_current_month - timedelta(days=1)
            
            return {
                "period_type": period,
                "start_date": get_month_start(3),
                "end_date": end_date,
                "label": "Last 3 months (Current month exclusive)"
            }
            
        if period == "last_6_months_current_month_inclusive":
            return {
                "period_type": period,
                "start_date": get_month_start(5),
                "end_date": current_date,
                "label": "Last 6 months (Current month inclusive)"
            }
            
        if period == "last_6_months_current_month_exclusive":
            end_date = first_day_of_current_month - timedelta(days=1)

            return {
                "period_type": period,
                "start_date": get_month_start(6),
                "end_date": end_date,
                "label": "Last 6 months (This month exclusive)"
            }
            
        if period == "current_year":
            return {
                "period_type": "current_year",
                "start_date": current_date.replace(
                    month=1,
                    day=1,
                ),
                "end_date": current_date,
                "label": "Current year"
            }
            
        if period == "last_year":
            last_year = current_date.year - 1

            return {
                "period_type": "last_year",
                "start_date": date(last_year, 1, 1),
                "end_date": date(last_year, 12, 31),
                "label": "Last year"
            }
            
    @staticmethod
    def generate_insights(user, summary, budget_overview, top_categories) -> list:
        insights = []
        total_expense = summary["total_expense"]
        balance = summary["balance"]
        
        exceeded = budget_overview["budgets_exceeded"]
        at_risk = budget_overview["budgets_at_risk"]
        total_budget = budget_overview["total_budget_amount"]
        
        most_used_category = CategoryService.get_most_used_category(user)
        
        # Most used Category insights
        insights.append(
            {
                "type": "info",
                "message": f"{most_used_category.name} is the most used category with {most_used_category.transaction_count} transactions"
            }
        )

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
                    "message": f"{at_risk} budget(s) is/are nearing their limit(s)."
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

        return insights

    @classmethod
    def get_user_analytics_data(cls, user) -> dict:
        
        # Gather raw querysets
        income_transactions = cls._get_current_period_income(user)
        expense_transactions = cls._get_current_period_expenses(user)
        budgets = cls._get_user_current_budgets(user)

        # Extract specific calculations using helper methods
        summary = cls.get_financial_summary(income_transactions, expense_transactions)
        top_categories = list(cls.get_top_categories(expense_transactions, limit=5))
        budget_overview = cls.get_budget_overview(expense_transactions, budgets)
        insights = cls.generate_insights(user, summary, budget_overview, top_categories)[:4]

        # Fetch independent services
        recent_transactions = (
            TransactionService
            .list_user_transactions(user)
            .order_by("-created_at")[:5]
        )

        # Pack into clean output schema
        return {
            "user": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "full_name": user.full_name,
            },
            "financial_overview": {
                "total_income": summary["total_income"],
                "total_expense": summary["total_expense"],
                "balance": summary["balance"],
            },
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
    def get_category_breakdown(cls, user, period):
        # Resolve the requested analytical period
        period_data = cls.period_resolver(period)
        
        start_date = period_data["start_date"]
        end_date = period_data["end_date"]
        
        # Retrieve user's expense type transactions 
        expense_transactions = cls._get_expense_transactions(user)
        
        # Apply date boundaries only when the period is date-bounded
        if start_date is not None and end_date is not None:
            expense_transactions = expense_transactions.filter(
                transaction_date__gte=start_date,
                transaction_date__lte=end_date,
            )
        
        # Calculate total expenses for the selected period
        total_expense = (
            expense_transactions.aggregate(
                total=Sum("amount")
            )["total"] or Decimal("0.00")
        )
        
        # Group transactions by category and calculate category totals
        categories = (expense_transactions
            .values(
                "category__id",
                "category__name",
            )
            .annotate(
                amount=Sum("amount"),
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
                    "percentage": round(percentage, 2),
                }
            )
            
        return {
            "period": period_data,
            "total_expense": total_expense,
            "categories": results,
        }
    
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
    
