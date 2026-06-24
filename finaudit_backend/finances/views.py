from rest_framework.views import APIView
from rest_framework import permissions, status
from django.core.exceptions import ValidationError

from .serializers import (
    CategoryResponseSerializer,
    CategoryCreateSerializer,
    CategoryUpdateSerializer,
    TransactionResponseSerializer,
    TransactionCreateSerializer,
    TransactionUpdateSerializer,
    BudgetResponseSerializer,
    BudgetCreateSerializer,
    BudgetUpdateSerializer,
)
from .services import CategoryService, TransactionService, BudgetService
from utils.response_helper_methods import success_response, error_response

 
# Create your views here.

#-----------------------------------------------
# Category Views
#-----------------------------------------------
class CategoryListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        categories = CategoryService.get_user_categories(request.user)
        
        serializer = CategoryResponseSerializer(categories, many=True)
        
        return success_response(
            message="Categories retrieved successfully.",
            data=serializer.data
        )
        
    def post(self, request):
        serializer = CategoryCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            category = CategoryService.create_category(
                user=request.user,
                **serializer.validated_data
            )
            
            return success_response(
                message="Category created successfully.",
                data=CategoryResponseSerializer(category).data,
                status_code=status.HTTP_201_CREATED
            )
            
        except ValueError as e:
            return error_response(str(e))

class CategoryDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, category_id):
        try:
            category = CategoryService.get_category(
                request.user,
                category_id
            )

            return success_response(
                message="Category retrieved successfully.",
                data=CategoryResponseSerializer(category).data
            )

        except ValueError as e:
            return error_response(
                str(e),
                status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, category_id):
        serializer = CategoryUpdateSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        try:
            category = CategoryService.update_category(
                request.user,
                category_id,
                **serializer.validated_data
            )

            return success_response(
                message="Category updated successfully.",
                data=CategoryResponseSerializer(category).data
            )

        except ValueError as e:
            return error_response(str(e))

    def delete(self, request, category_id):
        try:
            CategoryService.deactivate_category(
                request.user,
                category_id
            )

            return success_response(
                message="Category deactivated successfully."
            )

        except ValueError as e:
            return error_response(str(e))

#-----------------------------------------------
# Transaction Views
#-----------------------------------------------
class TransactionListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        filters = {
            'type': request.query_params.get('type'),
            'category': request.query_params.get('category'),
            'is_recurring': request.query_params.get('is_recurring'),
            'date_from': request.query_params.get('date_from'),
            'date_to': request.query_params.get('date_to'),
            'amount_min': request.query_params.get('amount_min'),
            'amount_max': request.query_params.get('amount_max'),
        }
        
        transactions = (
            TransactionService
            .list_user_transactions(request.user, filters)
        )

        serializer = TransactionResponseSerializer(transactions, many=True)

        return success_response(
            message="Transactions retrieved successfully.",
            data=serializer.data
        )

    def post(self, request):
        serializer = TransactionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            transaction = (
                TransactionService.create_transaction(
                    user=request.user,
                    **serializer.validated_data
                )
            )

            return success_response(
                message="Transaction created successfully.",
                data=TransactionResponseSerializer(
                    transaction
                ).data,
                status_code=status.HTTP_201_CREATED
            )

        except ValueError as e:
            return error_response(str(e))

class TransactionDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, transaction_id):
        try:
            transaction = (
                TransactionService.get_transaction(
                    request.user, 
                    transaction_id
                )
            )

            return success_response(
                message="Transaction retrieved successfully.",
                data=TransactionResponseSerializer(
                    transaction
                ).data
            )

        except ValueError as e:
            return error_response(
                str(e),
                status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, transaction_id):
        serializer = TransactionUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            transaction = (
                TransactionService.update_transaction(
                    request.user,
                    transaction_id,
                    **serializer.validated_data
                )
            )

            return success_response(
                message="Transaction updated successfully.",
                data=TransactionResponseSerializer(
                    transaction
                ).data
            )

        except ValueError as e:
            return error_response(str(e))

    def delete(self, request, transaction_id):
        try:
            TransactionService.deactivate_transaction(
                request.user,
                transaction_id
            )

            return success_response(
                message="Transaction deleted successfully."
            )

        except ValueError as e:
            return error_response(str(e))


#-----------------------------------------------
# Budget Views
#-----------------------------------------------
class BudgetListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        budgets = BudgetService.get_user_budgets(request.user)

        serializer = BudgetResponseSerializer(budgets, many=True)

        return success_response(
            message="Budgets retrieved successfully.",
            data=serializer.data
        )

    def post(self, request):
        serializer = BudgetCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            budget = BudgetService.create_budget(
                user=request.user,
                **serializer.validated_data
            )

            return success_response(
                message="Budget created successfully.",
                data=BudgetResponseSerializer(budget).data,
                status_code=status.HTTP_201_CREATED
            )

        except (ValueError, ValidationError) as e:
            return error_response(str(e))
        
class BudgetDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, budget_id):
        try:
            budget = BudgetService.get_budget(
                request.user,
                budget_id
            )

            return success_response(
                message="Budget retrieved successfully.",
                data=BudgetResponseSerializer(
                    budget
                ).data
            )

        except ValueError as e:
            return error_response(
                errors=str(e),
                status_code=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, budget_id):
        serializer = BudgetUpdateSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        try:
            budget = BudgetService.update_budget(
                request.user,
                budget_id,
                **serializer.validated_data
            )

            return success_response(
                message="Budget updated successfully.",
                data=BudgetResponseSerializer(
                    budget
                ).data
            )

        except (ValueError, ValidationError) as e:
            return error_response(str(e))

    def delete(self, request, budget_id):
        try:
            BudgetService.deactivate_budget(
                request.user,
                budget_id
            )

            return success_response(
                "Budget deleted successfully."
            )

        except ValueError as e:
            return error_response(str(e))
