from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.db.models import Q, Sum
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .models import Category, Transaction, Budget, TransactionTypeEnum

User = get_user_model()

class CategoryService:
    """
        Business rules:
           - Users can only manage their own categories
           - System categories are protected (no edit/delete)
           - Prevent duplicate category names (case-insensitive per user)
           - Prevent deletion if category is in use
           - Soft delete via is_active
    """
    
    @staticmethod
    def _ensure_authenticated(user):
        if not user or not user.is_authenticated:
            raise ValueError("Signup required to perform this operation.")
    
    @staticmethod
    def _validate_category_owner(user, category_id):
        category = CategoryService._get_category(user, category_id)
        
        return category
    
    @staticmethod
    def _get_owned_category(user, category_id):
        CategoryService._ensure_authenticated(user)
        
        try:
            return Category.objects.get(
                pk=category_id, 
                user=user
            )
        except Category.DoesNotExist:
            raise ValueError("Category not found")
        
    @staticmethod
    def _get_usable_category(user, category_id):
        CategoryService._ensure_authenticated(user)
        
        try:
            return Category.objects.get(
                Q(pk=category_id),
                Q(is_active=True),
                Q(user=user) | Q(is_system=True)
            )
        except Category.DoesNotExist:
            raise ValueError("Category not available for use.")
        
    @staticmethod
    def get_user_categories(user):
        CategoryService._ensure_authenticated(user)
        
        return Category.objects.filter(
            user=user,
            is_active=True
        ).order_by("-created_at")
        
    @staticmethod
    def get_category(user, category_id):
        CategoryService._ensure_authenticated(user)
        return CategoryService._get_owned_category(user, category_id)
        
    @staticmethod
    def _check_duplicate(user, name):
        exists = Category.objects.filter(
            user=user,
            name__iexact=name.strip(),
            is_active=True
        ).exists()
        
        if exists:
            raise ValueError("Category with this name already exists.")

    @staticmethod
    def _check_category_in_use(category):
        has_transactions = Transaction.objects.filter(category=category).exists()
        has_budgets = Budget.objects.filter(category=category).exists()
        
        if has_transactions or has_budgets:
            raise ValueError(
                "Category cannot be deleted because it's in use in transactions or budgets"
            )

    @staticmethod
    def create_category(user, name, type, is_system=False):
        CategoryService._ensure_authenticated(user)
        
        if is_system:
            raise ValueError("Cannot create built-in system categories.")
        
        CategoryService._check_duplicate(user, name)
        
        category = Category(
            user=user,
            name=name.strip(),
            type=type,
            is_active=True,
            is_system=False
        )
        
        category.full_clean(
            exclude=None,
            validate_unique=True,
            validate_constraints=True
        )
        category.save()
        return category
    
    @staticmethod
    @transaction.atomic
    def update_category(user, category_id, **updates):
        CategoryService._ensure_authenticated(user)
        
        category = CategoryService._get_owned_category(user, category_id)
        
        if category.is_system:
            raise ValueError("System built-in categories cannot be modified.")
        
        new_name = updates.get("name")
        if new_name and new_name.lower() != category.name.lower():
            CategoryService._check_duplicate(user, new_name)
            
        for field, value in updates.items():
            setattr(category, field, value)
        
        category.full_clean(
            exclude=None,
            validate_unique=True,
            validate_constraints=True
        )
        category.save()
        
        return category
        
    @staticmethod
    @transaction.atomic
    def deactivate_category(user, category_id):
        CategoryService._ensure_authenticated(user)
        
        category = CategoryService._get_owned_category(user, category_id)
        
        if category.is_system:
            raise ValueError("System built-in categories cannot be deactivated.")
        
        CategoryService._check_category_in_use(category)
        
        category.is_active = False
        category.save(update_fields=["is_active"])
        
        return category


class TransactionService:
    """
        Business rules:
            - Users can only manage their own transactions
            - Category must be active
            - Category must belong to user OR be a system category
            - Transaction type must match category type
            - Recurring transactions require:
                - frequency
                - next_due_date
            - Non-recurring transactions cannot have:
                - frequency
                - next_due_date
            - Transaction date cannot be in the future
            - next_due_date cannot be in the past
            - delete is soft via is_active
    """
    # ------------------------------------
    #   Internal helper methods
    # ------------------------------------
    @staticmethod
    def _get_transaction(user, transaction_id):
        CategoryService._ensure_authenticated(user)
        
        try:
            return Transaction.objects.select_related(
                "category"
            ).get(
                pk=transaction_id, 
                user=user
            )
        except Transaction.DoesNotExist:
            raise ValueError("Transaction not found.")
        
    @staticmethod
    def _validate_active_transaction(transaction):
        if not transaction.is_active:
            raise ValueError("Transaction has been deactivated.")
        
    @staticmethod
    def _validate_category(uscategory):
        if not category.is_active:
            raise ValueError("This category has been deactivated.")
        
    @staticmethod
    def _validate_category_type_match(category, transaction_type):
        if category.type != transaction_type:
            raise ValueError("Transaction type must match category type.")
        
    @staticmethod
    def _validate_recurring_fields(is_recurring, frequency, next_due_date):
        if is_recurring:
            if not frequency:
                raise ValueError("Recurring transactions require a frequency.")
            
            if not next_due_date:
                raise ValueError("Recurring transactions require a next due date.")
                
        else:
            if frequency:
                raise ValueError("Frequency can only be set for recurring transactions.")
                
            if next_due_date:
                raise ValueError("Next due date can only be set for recurring transactions.")
        
    @staticmethod
    def _validate_dates(transaction_date, next_due_date=None):
        today = timezone.now().date()
        
        if transaction_date > today:
            raise ValueError("Transaction date cannot be in the future.")
        
        if next_due_date and next_due_date < today:
            raise ValueError("Next due date cannot be in the past.")

    #-----------------------------
    #   Query methods
    #-----------------------------
    @staticmethod
    def get_user_transactions(user):
        CategoryService._ensure_authenticated(user)
        
        return Transaction.objects.filter(
            user=user,
            is_active=True
        ).select_related(
            "category"
        ).order_by(
            "type", 
            "category", 
            "is_recurring", 
            "-created_at"
        )
    
    @staticmethod
    def get_transaction(user, transaction_id):
        CategoryService._ensure_authenticated(user)
        
        return TransactionService._get_transaction(
            user,
            transaction_id
        )
    
    #-----------------------------
    #   Create
    #-----------------------------
    @staticmethod
    @transaction.atomic
    def create_transaction(
        user, 
        title, 
        type,
        amount,
        category_id, 
        description, 
        transaction_date,
        is_recurring=False,
        frequency=None,
        next_due_date=None
    ):
        CategoryService._ensure_authenticated(user)
        category = CategoryService._get_usable_category(user, category_id)
        
        TransactionService._validate_category(category)
        TransactionService._validate_category_type_match(category, type)
        TransactionService._validate_recurring_fields(
            is_recurring, 
            frequency, 
            next_due_date
        )
        TransactionService._validate_dates(transaction_date, next_due_date)
        
        transaction_obj = Transaction(
            user=user,
            title=title.strip(),
            amount=amount,
            type=type,
            category=category,
            description=description,
            transaction_date=transaction_date,
            is_recurring=is_recurring,
            frequency=frequency,
            next_due_date=next_due_date,
            is_active=True
        )
        
        transaction_obj.full_clean(
            exclude=None,
            validate_unique=True,
            validate_constraints=True
        )
        transaction_obj.save()
        return transaction_obj

    #------------------------------------------
    #   Update
    #------------------------------------------
    @staticmethod
    @transaction.atomic
    def update_transaction(user, transaction_id, **updates):
        CategoryService._ensure_authenticated(user)
        
        transaction_obj = (
            Transaction.objects
            .select_for_update()
            .get(
                pk=transaction_id,
                user=user
            )
        )
        
        TransactionService._validate_active_transaction(transaction_obj)
        
        new_category_id = updates.pop("category_id", None)
        
        if new_category_id:
            transaction_obj.category = (
                CategoryService._get_usable_category(
                    user,
                    new_category_id
                )
            )

        for field, value in updates.items():
            setattr(transaction_obj, field, value)
        
        category = transaction_obj.category
        if category: 
            TransactionService._validate_category(category)
            TransactionService._validate_category_type_match(
               category,
               transaction_obj.type
            )
            
        TransactionService._validate_recurring_fields(
            transaction_obj.is_recurring,
            transaction_obj.frequency,
            transaction_obj.next_due_date
        )
        
        TransactionService._validate_dates(
            transaction_obj.transaction_date,
            transaction_obj.next_due_date
        )
        
        transaction_obj.full_clean(
            exclude=None,
            validate_unique=True,
            validate_constraints=True
        )
        
        transaction_obj.save()
        return transaction_obj

    #----------------------------------------
    #   Delete(soft)
    #----------------------------------------
    @staticmethod
    @transaction.atomic
    def deactivate_transaction(user, transaction_id):
        CategoryService._ensure_authenticated(user)

        transaction_obj = (
            Transaction.objects
            .select_for_update()
            .get(
                pk=transaction_id,
                user=user
            )
        )
        
        TransactionService._validate_active_transaction(transaction_obj)

        transaction_obj.is_active = False
        transaction_obj.save(update_fields=["is_active"])
        
        return transaction_obj

    #--------------------------------------------
    #   Recurring helpers
    #--------------------------------------------
    @staticmethod
    def generate_next_occurrence(user, transaction_id):
        CategoryService._ensure_authenticated(user)

        transaction_obj = TransactionService._get_transaction(
            user,
            transaction_id
        )

        TransactionService._validate_active_transaction(transaction_obj)

        TransactionService._validate_recurring_fields(
            transaction_obj.is_recurring,
            transaction_obj.frequency,
            transaction_obj.next_due_date
        )
        
        current_due_date = transaction_obj.next_due_date

        if transaction_obj.frequency == "daily":
            return current_due_date + timedelta(days=1)

        if transaction_obj.frequency == "weekly":
            return current_due_date + timedelta(weeks=1)

        if transaction_obj.frequency == "biweekly":
            return current_due_date + timedelta(weeks=2)

        if transaction_obj.frequency == "monthly":
            return current_due_date + relativedelta(months=1)

        if transaction_obj.frequency == "quarterly":
            return current_due_date + relativedelta(months=3)

        if transaction_obj.frequency == "semiannual":
            return current_due_date + relativedelta(months=6)

        if transaction_obj.frequency == "yearly":
            return current_due_date + relativedelta(years=1)
        
        raise ValueError("Invalid transaction frequency.") 

    @staticmethod
    @transaction.atomic
    def pause_recurring_transaction(user, transaction_id):
        CategoryService._ensure_authenticated(user)
        
        transaction_obj = (
            Transaction.objects
            .select_for_update()
            .get(
                pk=transaction_id,
                user=user
            )
        )
        
        if not transaction_obj.is_recurring:
            raise ValueError("Transaction is not recurring.")
        
        transaction_obj.is_recurring = False
        transaction_obj.save(update_fields=["is_recurring"])

        return transaction_obj

    @staticmethod
    @transaction.atomic
    def resume_recurring_transaction(user, transaction_id):
        CategoryService._ensure_authenticated(user)
        
        transaction_obj = (
            Transaction.objects
            .select_for_update()
            .get(
                pk=transaction_id,
                user=user 
            )
        )
        
        if transaction_obj.is_recurring:
            raise ValueError("Transaction is already recurring.")
        
        if not transaction_obj.frequency:
            raise ValueError("Frequency must be configured before resuming.")
        
        if not transaction_obj.next_due_date:
            raise ValueError("Next due date must be configured before resuming.")
    
        transaction_obj.is_recurring = True
        transaction_obj.save(update_fields=["is_recurring"])

        return transaction_obj


class BudgetService:
    #----------------------------------
    #   Helper methods
    #----------------------------------
    @staticmethod
    def _get_budget_category(user, category_id):
        CategoryService._ensure_authenticated(user)
        
        category_obj = CategoryService._get_usable_category(user, category_id)

        return category_obj
    
    @staticmethod
    def _get_budget(user, budget_id):
        CategoryService._ensure_authenticated(user)
        
        try:
            return Budget.objects.select_related(
                "category"
            ).get(
                pk=budget_id,
                user=user
            )
        except Budget.DoesNotExist:
            raise ValueError("Budget not found.")
    
    @staticmethod
    def get_budget(user, budget_id):
        CategoryService._ensure_authenticated(user)
        return BudgetService._get_budget(user, budget_id)
    
    @staticmethod
    def _validate_active_budget(budget):
        if not budget.is_active:
            raise ValueError("Budget has been deactivated.")

    @staticmethod
    def get_user_budgets(user):
        CategoryService._ensure_authenticated(user)
        
        return Budget.objects.filter(
            user=user,
            is_active=True
        ).select_related(
            "category"
        ).order_by(
            "period_type",
            "start_date",
            "end_date",
            "-created_at"
        )

    @staticmethod
    def _check_duplicate(user, category, start_date, end_date, exclude_budget_id=None):
        budget_exists = Budget.objects.filter(
            user=user,
            category=category,
            start_date=start_date,
            end_date=end_date,
            is_active=True
        )
        
        if exclude_budget_id:
            budget_exists = budget_exists.exclude(pk=exclude_budget_id)
        
        if budget_exists:
            raise ValueError("Budget already exists.") 

    @staticmethod
    def _validate_budget_dates(start_date, end_date):
        if start_date > end_date:
            raise ValueError("The budget start date cannot be later than the end date.")

    @staticmethod
    def _validate_budget_period_type(period_type):
        budget_period_types = ['weekly', 'biweekly', 'monthly', 'quarterly', 'semiannual', 'yearly']

        if period_type not in budget_period_types:
            raise ValueError("Invalid budget period type")
    
    @staticmethod
    def _validate_overlapping_budgets(user, category, start_date, end_date, exclude_budget_id=None):
        overlapping_qs = Budget.objects.filter(
            user=user,
            category=category,
            is_active=True
        ).filter(
            # overlap condition:
            start_date__lte=end_date,
            end_date__gte=start_date
        )
        
        if exclude_budget_id:
            overlapping_qs = overlapping_qs.exclude(pk=exclude_budget_id)
            
        if overlapping_qs.exists():
            raise ValidationError("A budget already exists for this category and time period. Budgets cannot overlap.")
    
    #-----------------------------------
    #   Create
    #-----------------------------------    
    @staticmethod
    @transaction.atomic
    def create_budget(
        user,
        title,
        category,
        budget_amount,
        period_type,
        start_date,
        end_date
    ):
        CategoryService._ensure_authenticated(user)
        category = BudgetService._get_budget_category(user, category)
        BudgetService._validate_budget_dates(start_date, end_date)
        BudgetService._check_duplicate(
            user=user,
            category=category,
            start_date=start_date,
            end_date=end_date
        )
        
        BudgetService._validate_budget_period_type(period_type)
        budget_obj = Budget(
            user=user,
            title=title.strip(),
            category=category,
            budget_amount=budget_amount,
            period_type=period_type,
            start_date=start_date,
            end_date=end_date,
        )

        BudgetService._validate_overlapping_budgets(
            user=user,
            category=category,
            start_date=start_date,
            end_date=end_date
        )
        
        budget_obj.full_clean(
            exclude=None,
            validate_unique=True,
            validate_constraints=True
        )
        budget_obj.save()
        return budget_obj

    #-------------------------------------
    #   Update
    #-------------------------------------
    @staticmethod
    @transaction.atomic
    def update_budget(user, budget_id, **updates):
        CategoryService._ensure_authenticated(user)
        
        budget_obj = BudgetService._get_budget(user, budget_id)
        
        BudgetService._validate_active_budget(budget_obj)
        
        new_category_id = updates.pop("category", None)
        
        if new_category_id:
            budget_obj.category = (
                BudgetService._get_budget_category(
                    user, 
                    new_category_id
                )
            )
        
        for field, value in updates.items():
            setattr(budget_obj, field, value)
            
        category = budget_obj.category
        if category:
            BudgetService._get_budget_category(
                user,
                category.pk
            )
            
        BudgetService._validate_budget_dates(
            updates.get("start_date", budget_obj.start_date),
            updates.get("end_date", budget_obj.end_date)
        )
        
        BudgetService._validate_budget_period_type(
            updates.get("period_type", budget_obj.period_type)
        )
        
        BudgetService._check_duplicate(
            user=user,
            category=category,
            start_date=budget_obj.start_date,
            end_date=budget_obj.end_date,
            exclude_budget_id=budget_obj.pk
        )
        
        BudgetService._validate_overlapping_budgets(
            user=user,
            category=category,
            start_date=budget_obj.start_date,
            end_date=budget_obj.end_date,
            exclude_budget_id=budget_obj.pk
        )
        
        budget_obj.full_clean(
            exclude=None,
            validate_unique=True,
            validate_constraints=True
        )
        
        budget_obj.save()
        return budget_obj

    @staticmethod
    @transaction.atomic
    def deactivate_budget(user, budget_id):
        CategoryService._ensure_authenticated(user)
        
        budget_obj = BudgetService._get_budget(user, budget_id)

        BudgetService._validate_active_budget(budget_obj)
        
        budget_obj.is_active = False
        budget_obj.save(update_fields=["is_active"])
        
        return budget_obj
    
    #------------------------------------
    #   Budget tracking
    #------------------------------------
    @staticmethod
    def get_budget_spending(user, budget_id):
        CategoryService._ensure_authenticated(user)
        
        budget_obj = BudgetService._get_budget(user, budget_id)
        
        BudgetService._validate_active_budget(budget_obj)
        
        budget_transactions = Transaction.objects.filter(
            user=user,
            type=TransactionTypeEnum.EXPENSE,
            category=budget_obj.category,
            transaction_date__gte=budget_obj.start_date,
            transaction_date__lte=budget_obj.end_date,
        )
        
        amount_spent = budget_transactions.aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        amount_remaining = budget_obj.budget_amount - amount_spent
        percentage_used = (amount_spent / budget_obj.budget_amount) * 100
        
        return {
            "budget_amount": budget_obj.budget_amount,
            "amount_spent": amount_spent,
            "amount_remaining": amount_remaining,
            "percentage_used": round(percentage_used, 2)
        }
        
    @staticmethod
    def check_budget_status(budget, amount_spent, amount_remaining):
        
        budget_obj = BudgetService._get_budget(budget.user, budget.pk)
        
        BudgetService._validate_active_budget(budget_obj)
        
        if amount_spent > budget_obj.budget_amount:
            return {
                "status": "EXCEEDED!",
                "message": f"You have exceeded your budget limit - by {abs(amount_spent - budget_obj.budget_amount)}."
            }
        
        if amount_spent == budget_obj.budget_amount:
            return {
                "status": "REACHED!",
                "message": f"You have reached your budget limit - {budget_obj.budget_amount}."
            }
        
        if amount_spent >= (budget_obj.budget_amount * Decimal("0.8")):
            return {
                "status": "WARNING!",
                "message": f"You have spent 80% of your budget on {budget_obj.category.name}. Your remaining amount for this budget is {amount_remaining}."
            }
        
        return {
            "status": "NORMAL!",
            "message": f"You have {amount_remaining} remaining out of your {budget_obj.budget_amount} limit."
        }
        
    @staticmethod
    def check_budget_impact(user, category_id, amount, transaction_date):
        budget_obj = Budget.objects.filter(
            user=user,
            category=category_id,
            is_active=True,
            start_date__lte=transaction_date,
            end_date__gte=transaction_date
        ).first()
        
        if not budget_obj:
            return None
        
        spending = BudgetService.get_budget_spending(
            user=user,
            budget_id=budget_obj.pk
        )
        
        amount_spent = spending["amount_spent"] + amount
        amount_remaining = spending["budget_amount"] - amount_spent
        
        return BudgetService.check_budget_status(
            user=budget_obj.user,
            budget_id=budget_obj.pk,
            budget_amount=spending["budget_amount"],
            amount_spent=amount_spent,
            amount_remaining=amount_remaining,
        )
        
        