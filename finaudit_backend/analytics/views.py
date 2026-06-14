from rest_framework.views import APIView
from rest_framework import permissions

from .services import AnalyticsService
from utils.response_helper_methods import success_response

# Create your views here.
class AnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        analytics_data = AnalyticsService.get_user_analytics_data(request.user)
        
        return success_response(
            message= "Analytical data retrieved successfully.",
            data=analytics_data
        )