from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from allauth.socialaccount.signals import (
    social_account_added, 
    social_account_removed,
)

from .models import (
    UserSettings,
    Profile,
    UserSocialAccount,
    UserProviderEnum,
)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_related_objects(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        UserSettings.objects.create(user=instance)

        from allauth.socialaccount.models import SocialAccount
        has_social = SocialAccount.objects.filter(user=instance).exists()
        if not has_social:
            UserSocialAccount.objects.get_or_create(
                user=instance,
                provider=UserProviderEnum.LOCAL,
                defaults={
                    "provider_user_id": str(instance.pk),
                    "is_primary": True,
                    "email_at_provider_time": instance.email,
                },
            )

@receiver(social_account_added)
def create_social_account_record(sender, request, sociallogin, **kwargs):
    social = sociallogin.account
    email = sociallogin.user.email
    
    obj, created = UserSocialAccount.objects.update_or_create(
        provider=social.provider,
        provider_user_id=social.uid,
        defaults={
            "user": sociallogin.user,
            "is_primary": not UserSocialAccount.objects.filter(
                user=sociallogin.user
            ).exists(),
            "email_at_provider_time": email,
        },
    )
        
@receiver(social_account_removed)
def handle_social_account_removed(sender, request, socialaccount, **kwargs):
        user = socialaccount.user

        remaining_social = UserSocialAccount.objects.filter(
            user=user
        ).exclude(
            provider=socialaccount.provider
        ).count()

        has_local_password = user.has_usable_password()

        if remaining_social == 0 and not has_local_password:
            from allauth.exceptions import ImmediateHttpResponse
            from django.http import HttpResponseBadRequest
            raise ImmediateHttpResponse(
                HttpResponseBadRequest("You cannot remove your only login method.")
            )
            
        UserSocialAccount.objects.filter(
            user=user,
            provider=socialaccount.provider
        ).delete()
        
