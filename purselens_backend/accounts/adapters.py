from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount

from .models import UserSocialAccount


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return
        
        email = self._get_verified_email(sociallogin)
        if not email:
            return
        
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            existing_user = User.objects.get(email=email)
        except User.DoesNotExist:
            return
        
        if not existing_user.is_active:
            existing_user.is_active = True
            existing_user.is_verified = True
            existing_user.save(update_fields=['is_active', 'is_verified'])
            
            EmailAddress.objects.filter(
                user=existing_user,
                email=email
            ).update(verified=True)
            
        sociallogin.connect(request, existing_user)
        
    def _get_verified_email(self, sociallogin):
        for email in sociallogin.email_addresses:
            if email.verified and email.primary:
                return email
            
        for email in sociallogin.email_addresses:
            if email.verified:
                return email
        return None
    
    def is_auto_signup_allowed(self, request, sociallogin):
        return True
    
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        user.is_active = True
        user.is_verified = True
        user.save(update_fields=['is_active', 'is_verified'])
        
        return user





