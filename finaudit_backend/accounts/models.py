import uuid
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import default_storage
from django.utils import timezone
from datetime import timedelta


class UserProviderEnum(models.TextChoices):
    LOCAL = "local", "Local"
    GOOGLE = "google", "Google"
    APPLE = "apple", "Apple"
    FACEBOOK = "facebook", "Facebook"
    TIKTOK = "tiktok", "TikTok"
    TWITTER = "twitter", "Twitter"
    LINKEDIN = "linkedin", "LinkedIn"


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def __str__(self):
        return self.full_name
    
    
class UserSocialAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="social_account")
    provider = models.CharField(max_length=20)
    provider_user_id = models.CharField(max_length=200)
    is_primary = models.BooleanField()
    email_at_provider_time = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("provider", "provider_user_id")
    
    def __str__(self):
        return f"User: {self.user.first_name}, Provider: {self.provider}"
    
    
class UserSettings(models.Model):
    LANGUAGE_CHOICES = [
        ("en", "English"),
        ("fr", "French"),
        ("es", "Spanish"),
    ]
    
    CURRENCY_CHOICES = [
        ("GHS", "Ghana Cedi"),
        ("USD", "US Dollar"),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='settings')
    preferred_language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default="en")
    preferred_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="GHS")
    is_dark_theme = models.BooleanField(default=False)
    allow_email_notifications = models.BooleanField(default=True)
    allow_budget_alerts = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return f"{self.preferred_currency} {self.preferred_language}"
    
    
class EmailVerificationToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='verification_token')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(seconds=15)
        super().save(*args, **kwargs)
        
    @property
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f"Verification token for {self.user.email}, token: {self.token}"


def profile_picture_upload_path(instance, filename):
    return f"profile_picture/{instance.user.id}/{filename}"


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    
    
    profile_picture = models.ImageField(upload_to=profile_picture_upload_path, blank=True, null=True)
    
    TIMEZONE_CHOICES = [
        ("Africa/Accra", "Accra (GMT)"),
        ("Europe/London", "London"),
        ("Europe/Paris", "Paris"),
        ("America/New_York", "New York"),
        ("America/Los_Angeles", "Los Angeles"),
        ("Asia/Dubai", "Dubai"),
        ("Asia/Tokyo", "Tokyo"),
    ]
    
    timezone = models.CharField(max_length=50, choices=TIMEZONE_CHOICES, default="Africa/Accra")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        try:
            old_profile = Profile.objects.get(pk=self.pk)
            
            if old_profile.profile_picture != self.profile_picture:
                if old_profile.profile_picture:
                    default_storage.delete(
                        old_profile.profile_picture.path
                    )
        except Profile.DoesNotExist:
            pass
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.user.full_name

   