from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from axes.helpers import get_lockout_response
from axes.backends import AxesProxyHandler

from .utils import (
    generate_verfication_token, 
    send_verification_email,
    send_password_reset_email,
)

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    VerifyEmailSerializer,
    ResendVerificationEmailSerializer,
    UserDetailReadSerializer,
    UserDetailWriteSerializer,
    UserSettingsWriteSerializer,
    UserSettingsReadSerializer,
    UserProfileReadSerializer,
    ProfileWriteSerializer,
    ProfileReadSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)

from .throttles import (
    RegisterThrottle, 
    LoginThrottle, 
    PasswordResetThrottle,
)

User = get_user_model()


# Create your views here.
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [RegisterThrottle]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate token & send verification email
        raw_token = generate_verfication_token(user)
        send_verification_email(user, raw_token)
        
        return Response({
            "success": True,
            "message": "Account created successfully. Please check your email to verify your account.",
            "data": UserDetailReadSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data, context={})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.context['user']
        verification = serializer.context['verification']
        
        # Activate user
        user.is_active = True
        user.save()
        
        # Delete token - one time use
        verification.delete()
        
        # Issue JWT token now
        refresh = RefreshToken.for_user(user)
        return Response({
            "success": True,
            "message": "Email verified successfully",
            "data": {
                "token": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }
            }
        }, status=status.HTTP_200_OK)
   

class ResendVerificationView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [PasswordResetThrottle]
    
    def post(self, request):
        serializer = ResendVerificationEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                raw_token = generate_verfication_token(user)
                send_verification_email(user, raw_token)
        except User.DoesNotExist:
            pass    # Fail silently - don't reveal whether email exists
        
        return Response({
            "success": True,
            "message": "If an unverified account with that email exists, a new verification link has been sent."
        }, status=status.HTTP_200_OK)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [LoginThrottle]
    
    def post(self, request, *args, **kwargs):
        # Check if client is locked out before processing
        if AxesProxyHandler.is_locked(request, credentials={
            'username': request.data.get('email', '').lower()
        }):
            return Response({
                "success": False,
                "message": "Your account has been temporarily locked due to too many failed login attempts. Please try again in 30 minutes time.",
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed as e:
            return Response({
                "success": False,
                "message": str(e.detail)    
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        user = serializer.user
        tokens = serializer.validated_data
        
        return Response({
            "success": True,
            "message": "Login successful",
            "data": {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
                "tokens": {
                    "access": str(tokens['access']),
                    "refresh": str(tokens['refresh']),
                }
            }
        }, status=status.HTTP_200_OK)
    
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        refresh_token = request.data.get("refresh")
        
        if not refresh_token:
            return Response({
                "success": False,
                "detail": "Refresh token is required."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({
                "success": False,
                "detail": "Invalid or expired token."
            },status=status.HTTP_400_BAD_REQUEST)
            
        return Response({
            "success": True,
            "detail": "Logged out successfully."
        }, status=status.HTTP_200_OK)
        

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'patch', 'delete']
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDetailReadSerializer
        if self.request.method == 'PATCH':
            return UserDetailWriteSerializer
        return None

    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            "success": True,
            "message": "User details retrieved successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response({
            "success": True,
            "message": "Details updated successfully",
            "data": response.data
        }, status=status.HTTP_200_OK)
        
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        
        refresh_token = request.data.get('refresh')
        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except Exception:
                pass    # Token already invalid — not a critical failure
        
        return Response({
            "success": True,
            "message": "Account deactivated successfully.",
        }, status=status.HTTP_200_OK)
        

class UserSettingsView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'patch']
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSettingsReadSerializer
        return UserSettingsWriteSerializer
    
    def get_object(self):
        return self.request.user.settings
    
    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            "success": True,
            "message": "Settings retrieved successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response({
            "success": True,
            "message": "Settings updated successfully.",
            "data": response.data
        }, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'patch']
    
    def get_serializer_class(self):
       if self.request.method == 'GET':
           return UserProfileReadSerializer     # combined serializer
       return ProfileWriteSerializer
   
    def get_object(self):
        if self.request.method == 'GET':
            return self.request.user    
        return self.request.user.profile
    
    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            "success": True,
            "message": "Profile retrieved successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response({
            "success": True,
            "message": "Profile updated successfully",
            "data": response.data
        }, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        
        return Response({
            "success": True,
            "detail": "Password changed successfully."
        }, status=status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [PasswordResetThrottle]
    
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
            send_password_reset_email(user, request)
        except User.DoesNotExist:
            pass    # Fail silently — don't reveal whether email exists
        
        return Response({
            "success": True,
            "detail": "If an account with that email exists, a reset link has been sent."
            },status=status.HTTP_200_OK)
        
        
class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({
            "success": True,
            "detail": "Password reset successfully."
        }, status=status.HTTP_200_OK)

