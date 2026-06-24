from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination

from .models import AuditLog, AuditLogEnum
from .serializers import AuditLogSerializer

# Create your views here.
class AuditLogPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
    
class UserActivityLogListView(generics.ListAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = AuditLogPagination
    
    def get_queryset(self):
        qs = AuditLog.objects.filter(user=self.request.user)
        action = self.request.query_params.get("action")
        if action and action in AuditLogEnum.values:
            qs = qs.filter(action=action)
        
        return qs

class UserActivityLogDetailView(generics.RetrieveAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return AuditLog.objects.filter(user=self.request.user)
    
class AdminActivityLogListView(generics.ListAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = AuditLogPagination
    
    def get_queryset(self):
        qs = AuditLog.objects.select_related("user").all()
        action = self.request.query_params.get("action")
        user_id = self.request.query_params.get("user_id")
        target_model = self.request.query_params.get("target_model")
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")
        
        if action and action in AuditLogEnum.values():
            qs = qs.filter(action=action)
            
        if user_id:
            qs = qs.filter(user_id=user_id)

        if target_model:
            qs = qs.filter(target_model__iexact=target_model)
            
        if date_from:
            qs = qs.filter(created_at__date__gte=date_from)
            
        if date_to:
            qs = qs.filter(created_at__date__lte=date_to)
            
        return qs
