from .models import AuditLog

def get_client_ip(request) -> str | None:
    """
        Extract real client IP, respecting reverse-proxy X-Forwarded-For headers
    """
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")

def log_activity(
    user,
    action: str,
    target_model: str = "",
    target_id=None,
    description: str = "",
    old_values: dict | None = None,
    new_values: dict | None = None,
    request=None
) -> AuditLog:
    user_ip, user_agent = None, ""
    if request:
        user_ip = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")[:256]
        
    return AuditLog.objects.create(
        user=user,
        action=action,
        target_model=target_model,
        target_id=target_id,
        description=description,
        old_values=old_values,
        new_values=new_values,
        ip_address=user_ip,
        user_agent=user_agent,
    )