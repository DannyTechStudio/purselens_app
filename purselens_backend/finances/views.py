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
    TransactionFilterSerializer,
    BudgetResponseSerializer,
    BudgetCreateSerializer,
    BudgetUpdateSerializer,
)

from .pagination import TransactionPagination, CategoryPagination, BudgetPagination
from .services import CategoryService, TransactionService, BudgetService
from utils.response_helper_methods import success_response, error_response

 
# Create your views here.

#-----------------------------------------------
#   Category Views
#-----------------------------------------------
class CategoryListCreateView(APIView):
    # Allow only authenticated users
    permission_classes = [permissions.IsAuthenticated]
    
    # Read category data
    def get(self, request):
        # Instantiate category metadata
        filters = {
            'type': request.query_params.get('type'),
            'is_system': request.query_params.get('is_system'),
        }
        
        # Fetch user-owned category
        categories = CategoryService.get_user_categories(
            request.user, 
            filters
        )
        
        # Instantiate the category pagination class
        paginator = CategoryPagination()
        
        # Paginate the queryset
        paginated_categories = paginator.paginate_queryset(
            categories,
            request, 
            view=self
        )
        
        # Serialize only the paginated data 
        serializer = CategoryResponseSerializer(
            paginated_categories, 
            many=True
        )
        
        paginated_data = {
            "count": paginator.page.paginator.count,
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "results": serializer.data,        
        }
        
        return success_response(
            message="Categories retrieved successfully.",
            data=paginated_data
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
    # Allow only authenticated users
    permission_classes = [permissions.IsAuthenticated]

    # Read transaction data
    def get(self, request):
        # Validate transaction filtering parameters
        filter_serializer = TransactionFilterSerializer(
            data=request.query_params
        )
        
        # Run validation and raise an exception if invalid
        filter_serializer.is_valid(raise_exception=True)
        
        # Retrieve validated filter values
        filters = filter_serializer.validated_data
        
        # Fetch user-owned transaction data
        transactions = (
            TransactionService
            .list_user_transactions(request.user, filters)
        )
        
        # Instantiate the transaction pagination class
        paginator = TransactionPagination()
        
        # Paginate the queryset
        paginated_transactions = paginator.paginate_queryset(
            transactions,
            request,
            view=self
        )

        # Serialize the paginated transactions
        serializer = TransactionResponseSerializer(
            paginated_transactions,
            many=True
        )
        
        pagination_data = {
            "count": paginator.page.paginator.count,
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "results": serializer.data,
        }

        return success_response(
            message="Transactions retrieved successfully.",
            data=pagination_data
        )

    # Create transaction
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
#   Budget Views
#-----------------------------------------------
class BudgetListCreateView(APIView):
    # Allow only authenticated user
    permission_classes = [permissions.IsAuthenticated]

    # Read budget data
    def get(self, request):
        # Instantiate filtering metadata
        filters = {
            'category': request.query_params.get('category'),
            'period_type': request.query_params.get('period_type'),
        }
        
        # Fetch user-owned budget data
        budgets = BudgetService.get_user_budgets(
            request.user, 
            filters
        )
        
        # Instantiate the budget pagination class
        paginator = BudgetPagination()
        
        # Paginate the queryset
        paginated_budgets = paginator.paginate_queryset(
            budgets,
            request,
            view=self
        )

        # Serialize the paginated data
        serializer = BudgetResponseSerializer(
            paginated_budgets, 
            many=True
        )
        
        paginated_data = {
            "count": paginator.page.paginator.count,
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "results": serializer.data
        }

        return success_response(
            message="Budgets retrieved successfully.",
            data=paginated_data
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
