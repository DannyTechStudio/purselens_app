from django.contrib import admin

from .models import Category, Transaction, Budget

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "type", "is_system", "is_active")
    list_filter = ("type", "is_system", "is_active")
    search_fields = ("name",)
    
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "amount", "type", "transaction_date", "is_active")
    list_filter = ("type", "is_recurring", "is_active")
    search_fields = ("title",)

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "budget_amount", "period_type", "is_active")
    list_filter = ("period_type", "is_active")
    search_fields = ("title",)

