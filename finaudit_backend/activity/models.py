import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Audit log enum
class AuditLogEnum(models.TextChoices):
    CREATE = "create", "Create"
    UPDATE = "update", "Update"
    DELETE = "delete", "Delete"
    LOGIN = "login", "Login"
    LOGOUT = "logout", "Logout"
    PASSWORD_CHANGE = ("password_change", "Password Change")
    EMAIL_VERIFY = ("email_verify", "Email Verify")


# Create your models here.
class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='activity_logs', null=True, blank=True)
    action = models.CharField(max_length=20, choices=AuditLogEnum.choices)
    target_model = models.CharField(max_length=20, null=True, blank=True)
    target_id = models.UUIDField(null=True, blank=True)
    description = models.TextField()
    old_values = models.JSONField(null=True, blank=True)
    new_values = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.action} by {self.user}"
        
