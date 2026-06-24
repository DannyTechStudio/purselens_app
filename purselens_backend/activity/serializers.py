from rest_framework import serializers
from .models import AuditLog

class AuditLogSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user_email", read_only=True, default=None)
    user_full_name = serializers.CharField(source="user.get_full_name", read_only=True, default=None)
    action_display = serializers.CharField(source="get_action_display", read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            "id",
            "user",
            "user_email",
            "user_full_name",
            "action",
            "action_display",
            "target_model",
            "target_id",
            "descritpion",
            "old_values",
            "new_values",
            "ip_address",
            "user_agent",
            "created_at",
        ]
        read_only_fields = fields
    