import uuid
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

from .validators import validate_max_words

User = settings.AUTH_USER_MODEL


# Enums
class CategoryTypeEnum(models.TextChoices):
    INCOME = 'income', 'Income'
    EXPENSE = 'expense', 'Expense'


class TransactionTypeEnum(models.TextChoices):
    INCOME = 'income', 'Income'
    EXPENSE = 'expense', 'Expense'


class TransactionFrequencyEnum(models.TextChoices):
    DAILY = 'daily', 'Daily'
    WEEKLY = 'weekly', 'Weekly'
    BIWEEKLY = 'biweekly', 'Bi-Weekly'
    MONTHLY = 'monthly', 'Monthly'
    QUARTERLY = 'quarterly', 'Quarterly'
    SEMIANNUAL = 'semiannual', 'Semi-Annual'
    YEARLY = 'yearly', 'Yearly'


class BudgetPeriodEnum(models.TextChoices):
    WEEKLY = 'weekly', 'Weekly'
    BIWEEKLY = 'biweekly', 'Bi-Weekly'
    MONTHLY = 'monthly', 'Monthly'
    QUARTERLY = 'quarterly', 'Quarterly'
    SEMIANNUAL = 'semiannual', 'Semi-Annual'
    YEARLY = 'yearly', 'Yearly'


# Create your models here.
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='categories')
    name = models.CharField(max_length=50)
    type = models.CharField(choices=CategoryTypeEnum.choices, max_length=10)
    is_system = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'],
                name='unique_user_category'
            )
        ]
        ordering = ['-created_at']

    def __str__(self):
        owner = self.user.email if self.user else "SYSTEM"
        return f"Category: {self.name} ({owner})"
        

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    title = models.CharField(max_length=50)
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[
            MinValueValidator(
                0.01,
                message="Transaction amount must be greater than zero."
            )
        ]
    )
    type = models.CharField(choices=TransactionTypeEnum.choices, max_length=10)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='transactions'
    )
    description = models.CharField(max_length=1000, validators=[validate_max_words], null=True, blank=True)
    transaction_date = models.DateField()
    is_recurring = models.BooleanField(default=False)
    frequency = models.CharField(choices=TransactionFrequencyEnum.choices, max_length=15, null=True, blank=True)
    next_due_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['transaction_date', '-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['transaction_date']),
            models.Index(fields=['user', 'transaction_date']),
        ]
    
    def clean(self):
        errors = {}
        
        if self.is_recurring:
            if not self.frequency: 
                errors["frequency"] = (
                    "Recurring transactions require a frequency."
                )
            
            if not self.next_due_date:
                errors["next_due_date"] = (
                    "Recurring transactions require a next due date."
                )
                
        else:
            if self.frequency: 
                errors["frequency"] = (
                    "Frequency can only be set for recurring transactions."
                )
                
            if self.next_due_date:
                errors["next_due_date"] = (
                    "Next due date can only be set for recurring transactions."
                )
        
        today = timezone.now().date()
        
        if self.next_due_date and self.next_due_date < today:
            errors["next_due_date"] = (
                "Next due date for a recurring transaction can't be in the past."
            )
            
        if errors:
            raise ValidationError(errors)
            
    def __str__(self):
        return f"Transaction: {self.title} ({self.amount})"
        
        

class Budget(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    title = models.CharField(max_length=50)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL,
        null=True, blank=True, 
        related_name='budgets'
    )
    budget_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[
            MinValueValidator(
                0.01,
                message="Budget amount must be greater than zero."
            )
        ]
    )
    period_type = models.CharField(choices=BudgetPeriodEnum.choices, max_length=15)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'category', 'start_date', 'end_date'],
                name='unique_user_budget'  
            )
        ]
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['period_type']),
            models.Index(fields=['user', 'period_type']),
        ]
        
    def clean(self):
        errors = {}
        
        if self.start_date > self.end_date:
            errors["start_date"] = (
                "Budgets start date cannot be later than the end date."
            )
            
        if errors:
            raise ValidationError(errors)
        
    def __str__(self):
        return f"Budget: {self.title} ({self.budget_amount})"

