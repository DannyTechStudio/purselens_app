from django.utils import timezone
from django.db import transaction
from django.db.models import Q, Sum
from decimal import Decimal

from .models import (
    Category,
    Transaction,
    Budget,
    TransactionTypeEnum
)


#------------------------------------
# Category Service
#------------------------------------
class CategoryService:
    @staticmethod
    def _get_owned_category(user, category_id):
        try:
            return Category.objects.get(pk=category_id, user=user)
        except Category.DoesNotExist:
            raise ValueError("Category not found")

    @staticmethod
    def _get_usable_category(user, category_id):
        try:
            return Category.objects.get(
                Q(pk=category_id),
                Q(is_active=True),
                Q(user=user) | Q(is_system=True)
            )
        except Category.DoesNotExist:
            raise ValueError("Category not available for use.")

    @staticmethod
    def get_category(user, category_id):
        try:
            return Category.objects.get(pk=category_id, user=user)
        except Category.DoesNotExist:
            raise ValueError("Category not found")

    @staticmethod
    def get_user_categories(user, filters: dict = None):
        qs = Category.objects.filter(
            user=user,
            is_active=True
        ).order_by("-created_at")
        
        if filters:
            if category_type := filters.get('type'):
                qs = qs.filter(type=category_type)
                
            if is_system := filters.get('is_system'):
                qs = qs.filter(is_system=is_system)
                
        return qs

    @staticmethod
    def _check_duplicate(user, name):
        if Category.objects.filter(
            user=user,
            name__iexact=name.strip(),
            is_active=True
        ).exists():
            raise ValueError("Category already exists.")

    @staticmethod
    def _check_category_in_use(category):
        if Transaction.objects.filter(category=category).exists() or \
           Budget.objects.filter(category=category).exists():
            raise ValueError("Category is in use.")

    @staticmethod
    def create_category(user, name, type, is_system=False):
        if is_system:
            raise ValueError("Cannot create system category.")

        CategoryService._check_duplicate(user, name)

        category = Category(
            user=user,
            name=name.strip(),
            type=type,
            is_active=True,
            is_system=False
        )

        category.full_clean()
        category.save()
        return category

    @staticmethod
    @transaction.atomic
    def update_category(user, category_id, **updates):
        category = CategoryService._get_owned_category(user, category_id)

        if category.is_system:
            raise ValueError("System category cannot be modified.")

        new_name = updates.get("name")
        if new_name and new_name.lower() != category.name.lower():
            CategoryService._check_duplicate(user, new_name)

        for field, value in updates.items():
            setattr(category, field, value)

        category.full_clean()
        category.save()
        return category

    @staticmethod
    @transaction.atomic
    def deactivate_category(user, category_id):
        category = CategoryService._get_owned_category(user, category_id)

        if category.is_system:
            raise ValueError("Cannot deactivate system category.")

        CategoryService._check_category_in_use(category)

        category.is_active = False
        category.save(update_fields=["is_active"])
        return category


#------------------------------------
# Transaction Service
#------------------------------------
class TransactionService:
    @staticmethod
    def _get_transaction(user, transaction_id):
        try:
            return Transaction.objects.select_related("category").get(
                pk=transaction_id,
                user=user
            )
        except Transaction.DoesNotExist:
            raise ValueError("Transaction not found.")
    
    @staticmethod
    def get_transaction(user, transaction_id):
        try:
            return Transaction.objects.get(pk=transaction_id, user=user)
        except Transaction.DoesNotExist:
            raise ValueError("Transaction not found")

    @staticmethod
    def _validate_active_transaction(transaction):
        if not transaction.is_active:
            raise ValueError("Transaction is inactive.")

    @staticmethod
    def _validate_category(category):
        if not category.is_active:
            raise ValueError("Category inactive.")

    @staticmethod
    def _validate_category_type_match(category, transaction_type):
        if category.type != transaction_type:
            raise ValueError("Transaction type mismatch.")

    @staticmethod
    def _validate_recurring_fields(is_recurring, frequency, next_due_date):
        if is_recurring:
            if not frequency or not next_due_date:
                raise ValueError("Missing recurring fields.")
        else:
            if frequency or next_due_date:
                raise ValueError("Invalid recurring fields.")

    @staticmethod
    def _validate_dates(transaction_date, next_due_date=None):
        today = timezone.now().date()

        if transaction_date > today:
            raise ValueError("Future transaction not allowed.")

        if next_due_date and next_due_date < today:
            raise ValueError("Invalid due date.")

    @staticmethod
    def list_user_transactions(user, filters: dict = None):
        qs = Transaction.objects.filter(
            user=user,
            is_active=True
        ).select_related("category")
        
        if filters:
            if transaction_type := filters.get('type'):
                qs = qs.filter(type=transaction_type)
                
            if category := filters.get('category'):
                qs = qs.filter(category=category)
                
            if is_recurring := filters.get('is_recurring'):
                qs = qs.filter(is_recurring=is_recurring)
                
            if date_from := filters.get('date_from'):
                qs = qs.filter(transaction_date__gte=date_from)
                 
            if date_to := filters.get('date_to'):
                qs = qs.filter(transaction_date__lte=date_to)
                
            if (amount_min := filters.get('amount_min')) is not None:
                qs = qs.filter(amount__gte=amount_min)
                
            if amount_max := filters.get('amount_max'):
                qs = qs.filter(amount__gte=amount_max)

        return qs

    @staticmethod
    def create_transaction(user, **data):
        category = CategoryService._get_usable_category(user, data["category_id"])

        TransactionService._validate_category(category)
        TransactionService._validate_category_type_match(category, data["type"])
        TransactionService._validate_recurring_fields(
            data.get("is_recurring", False),
            data.get("frequency"),
            data.get("next_due_date")
        )
        TransactionService._validate_dates(
            data["transaction_date"],
            data.get("next_due_date")
        )

        transaction_obj = Transaction(
            user=user,
            title=data["title"].strip(),
            amount=data["amount"],
            type=data["type"],
            category=category,
            description=data.get("description"),
            transaction_date=data["transaction_date"],
            is_recurring=data.get("is_recurring", False),
            frequency=data.get("frequency"),
            next_due_date=data.get("next_due_date"),
            is_active=True
        )

        transaction_obj.full_clean()
        transaction_obj.save()
        return transaction_obj
    
    @staticmethod
    @transaction.atomic
    def update_transaction(user, transaction_id, **updates):
        transaction = TransactionService._get_transaction(user, transaction_id)
        
        TransactionService._validate_active_transaction(transaction)
        
        for field, value in updates.items():
            setattr(transaction, field, value)
            
        TransactionService._validate_recurring_fields(
            is_recurring=transaction.is_recurring,
            frequency=transaction.frequency,
            next_due_date=transaction.next_due_date
        )
            
        TransactionService._validate_dates(
            transaction_date=transaction.transaction_date,
            next_due_date=transaction.next_due_date
        )
            
        TransactionService._validate_category_type_match(
            transaction.category,
            transaction.type
        )
            
        transaction.full_clean()
        transaction.save()
        return transaction

    @staticmethod
    @transaction.atomic
    def deactivate_transaction(user, transaction_id):
        transaction_obj = TransactionService._get_transaction(user, transaction_id)

        TransactionService._validate_active_transaction(transaction_obj)

        transaction_obj.is_active = False
        transaction_obj.save(update_fields=["is_active"])
        return transaction_obj


#------------------------------------
# Budget Service
#------------------------------------
class BudgetService:
    @staticmethod
    def _get_budget(user, budget_id):
        try:
            return Budget.objects.select_related("category").get(
                pk=budget_id,
                user=user
            )
        except Budget.DoesNotExist:
            raise ValueError("Budget not found.")
        
    @staticmethod
    def get_budget(user, budget_id):
        try:
            return Budget.objects.get(pk=budget_id, user=user)
        except Budget.DoesNotExist:
            raise ValueError("Budget not found")

    @staticmethod
    def get_user_budgets(user, filters: dict = None):
        qs = Budget.objects.filter(
            user=user,
            is_active=True
        ).select_related("category")
        
        if filters:
            if category := filters.get('category'):
                qs = qs.filter(category=category)
                
            if period_type := filters.get('period_type'):
                qs = qs.filter(period_type=period_type)
                
        return qs

    @staticmethod
    def _validate_active_budget(budget):
        if not budget.is_active:
            raise ValueError("Category inactive.")

    @staticmethod
    def _check_duplicate(user, category, start_date, end_date, exclude_id=None):
        qs = Budget.objects.filter(
            user=user,
            category=category,
            start_date=start_date,
            end_date=end_date,
            is_active=True
        )

        if exclude_id:
            qs = qs.exclude(pk=exclude_id)

        if qs.exists():
            raise ValueError("Duplicate budget.")

    @staticmethod
    def _validate_budget_dates(start_date, end_date):
        if start_date > end_date:
            raise ValueError("Invalid date range.")

    @staticmethod
    def _validate_budget_period_type(period_type):
        allowed = ['weekly','biweekly','monthly','quarterly','semiannual','yearly']
        if period_type not in allowed:
            raise ValueError("Invalid period.")

    @staticmethod
    def _validate_overlapping_budgets(user, category, start_date, end_date, exclude_id=None):
        qs = Budget.objects.filter(
            user=user,
            category=category,
            is_active=True,
            start_date__lte=end_date,
            end_date__gte=start_date
        )

        if exclude_id:
            qs = qs.exclude(pk=exclude_id)

        if qs.exists():
            raise ValueError("Overlapping budget detected.")

    @staticmethod
    @transaction.atomic
    def create_budget(user, **data):
        category = CategoryService._get_usable_category(user, data["category_id"])

        BudgetService._validate_budget_dates(data["start_date"], data["end_date"])
        BudgetService._check_duplicate(
            user, category,
            data["start_date"],
            data["end_date"]
        )
        BudgetService._validate_budget_period_type(data["period_type"])

        budget = Budget(
            user=user,
            title=data["title"].strip(),
            category=category,
            budget_amount=data["budget_amount"],
            period_type=data["period_type"],
            start_date=data["start_date"],
            end_date=data["end_date"]
        )

        BudgetService._validate_overlapping_budgets(
            user, category,
            data["start_date"],
            data["end_date"]
        )

        budget.full_clean()
        budget.save()
        return budget
    
    @staticmethod
    @transaction.atomic
    def update_budget(user, budget_id, **updates):
        budget = BudgetService._get_budget(user, budget_id)
        
        BudgetService._validate_active_budget(budget)
        
        for field, value in updates.items():
            setattr(budget, field, value)
            
        BudgetService._check_duplicate(
            user=user,
            category=budget.category,
            start_date=budget.start_date,
            end_date=budget.end_date,
            exclude_id=budget.pk
        )
            
        if budget.start_date or budget.end_date:
            BudgetService._validate_budget_dates(
                budget.start_date,
                budget.end_date
            )
            
        if budget.period_type:
            BudgetService._validate_budget_period_type(
                budget.period_type
            )
            
        BudgetService._validate_overlapping_budgets(
            user=user,
            category=budget.category,
            start_date=budget.start_date,
            end_date=budget.end_date,
            exclude_id=budget.pk
        )
            
        budget.full_clean()
        budget.save()
        return budget
    
    @staticmethod
    @transaction.atomic
    def deactivate_budget(user, budget_id):
        budget_obj = BudgetService._get_budget(user, budget_id)
        
        BudgetService._validate_active_budget(budget_obj)
        
        budget_obj.is_active = False
        budget_obj.save(update_fields=["is_active"])
        return budget_obj

    @staticmethod
    def get_budget_spending(user, budget_id):
        budget = BudgetService._get_budget(user, budget_id)

        qs = Transaction.objects.filter(
            user=user,
            type=TransactionTypeEnum.EXPENSE,
            category=budget.category,
            transaction_date__range=[budget.start_date, budget.end_date]
        )

        spent = qs.aggregate(total=Sum("amount"))["total"] or 0
        remaining = budget.budget_amount - spent

        return {
            "budget_amount": budget.budget_amount,
            "amount_spent": spent,
            "amount_remaining": remaining,
            "percentage_used": round((spent / budget.budget_amount) * 100, 2)
        }

    @staticmethod
    def check_budget_status(budget, amount_spent):
        if amount_spent > budget.budget_amount:
            return {"status": "EXCEEDED"}

        if amount_spent == budget.budget_amount:
            return {"status": "REACHED"}

        if amount_spent >= (budget.budget_amount * Decimal("0.8")):
            return {"status": "WARNING"}

        return {"status": "NORMAL"}

    @staticmethod
    def check_budget_impact(user, category_id, amount, transaction_date):
        budget = Budget.objects.filter(
            user=user,
            category=category_id,
            is_active=True,
            start_date__lte=transaction_date,
            end_date__gte=transaction_date
        ).first()

        if not budget:
            return None

        spending = BudgetService.get_budget_spending(user, budget.id)

        new_spent = spending["amount_spent"] + amount
        remaining = budget.budget_amount - new_spent

        return BudgetService.check_budget_status(
            budget,
            new_spent,
            remaining
        )
        
        