import hashlib
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed as DRFAuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from axes.backends import AxesProxyHandler
from axes.helpers import get_client_ip_address
from django.contrib.auth.signals import user_login_failed

from .models import (
    UserSettings,
    Profile,
    EmailVerificationToken,
)

User = get_user_model()

# Create your serializers here.
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']

    def validate_email(self, value):
        return value.lower()
    
    def validate_password(self, pwd):
        validate_password(pwd)
        return pwd
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField()
    
    def validate_token(self, raw_token):
        raw_token = raw_token.strip()
        hash_token = hashlib.sha256(raw_token.encode()).hexdigest()
        
        stored = EmailVerificationToken.objects.first()
        
        try:
            verification = EmailVerificationToken.objects.select_related('user').get(token=hash_token)
        except EmailVerificationToken.DoesNotExist:
            raise serializers.ValidationError("Invalid verification link")
        
        if verification.is_expired:
            raise serializers.ValidationError("Verification link has expired. Request for a new one.")

        if verification.user.is_active:
            raise serializers.ValidationError("Account already verified.")
        
        self.context['user'] = verification.user
        self.context['verification'] = verification
        
        return raw_token


class ResendVerificationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        return value.lower()


class LoginSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    
    def validate(self, attrs):
        request = self.context.get('request')
        email = attrs.get('email', '').lower()
        
        try:
            data = super().validate(attrs)
            
            # Reset failed attempts on successful login
            AxesProxyHandler.reset_attempts(
                ip_address=get_client_ip_address(request),
                username=email
            )
            return data
        except Exception:
            
            # Signal axes about login failure
            user_login_failed.send(
                sender=User,
                request=request,
                credentials={'username': email}
            )
            
            try:
                user = User.objects.get(email=email)
                if not user.is_active:
                    raise AuthenticationFailed("Account not verified. Please check your email or request a new verification link.")
            except User.DoesNotExist:
                pass
            
            raise DRFAuthenticationFailed("Invalid email or password. Please try again.")
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        return token


class UserDetailReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'is_active', 'is_verified', 'created_at', 'updated_at']
        
        
class UserDetailWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UserSettingsReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = ['id', 'user', 'preferred_language', 'preferred_currency', 'is_dark_theme', 'allow_email_notifications', 'allow_budget_alerts', 'created_at', 'updated_at']


class UserSettingsWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        exclude = ['user', 'created_at', 'updated_at']


class ProfileReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'profile_picture', 'timezone', 'created_at', 'updated_at']


class ProfileWriteSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    
    class Meta:
        model = Profile
        fields = ['profile_picture', 'timezone']
        
    def validate_profile_picture(self, image):
        allowed_types = ['image/jpeg', 'image/png', 'image/webp']
        max_size = 2 * 1024 * 1024      # 2MB
        
        if image.content_type not in allowed_types:
            raise serializers.ValidationError("Unsupported imge type. Only JPEG, PNG, and WEBP images are allowed.")
        if image.size > max_size:
            raise serializers.ValidationError("Image size must not exceed 2MB.")
        return image
        

class UserProfileReadSerializer(serializers.ModelSerializer):
    profile = ProfileReadSerializer(read_only=True)
    settings = UserSettingsReadSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'profile', 'settings']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
    
    def validate_new_password(self, value):
        validate_password(value)
        return value
    
    def validate(self, data):
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError("New password must be different from the old password.")
        return data
    
    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        return value.lower()
    
    
class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    
    def validate_new_password(self, value):
        validate_password(value)
        return value
    
    def validate(self, data):
        # Decode uid and fetch user
        try:
            user_id = force_str(urlsafe_base64_decode(data['uid']))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid reset link.")
        
        # Validate token
        if not PasswordResetTokenGenerator().check_token(user, data['token']):
            raise serializers.ValidationError("Reset link is invalid or expired.")
        
        # Attach user to validated data for view
        data['user'] = user
        return data
        
