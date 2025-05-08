from django.urls import path
from .views import (
    RegistrationApiView, CustomAuthToken, CustomDeleteToken,
    CustomChangePasswordView, CustomProfileUserView, CustomActivationView,
    CustomActivationResendView, CustomResetPasswordView
)
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)
# ======================================================================================================================
# Setting the application namespace to 'api-v1' for better URL reversibility and organization
app_name = 'api-v1'

# Defining URL patterns for authentication and user management
urlpatterns = [
    # Registration API endpoint
    path('registeration/', RegistrationApiView.as_view(), name='register'),
    # - Handles user registration requests.

    # Account Activation API endpoint (via token confirmation)
    path('activation/confirm/<str:token>/', CustomActivationView.as_view(), name='activation'),
    # - Confirms user account activation using a unique token.

    # Resend Activation Email API endpoint
    path('activation/resend/', CustomActivationResendView.as_view(), name='resend'),
    # - Resends the activation email if needed.

    # Password Change API endpoint
    path('change_password/', CustomChangePasswordView.as_view(), name='change_password'),
    # - Allows users to securely change their password.

    # Password Reset API endpoint
    path('rest/password/', CustomResetPasswordView.as_view(), name='rest_password'),
    # - Enables users to reset their password via email verification.

    # Login Token API endpoints
    path('token/login/', CustomAuthToken.as_view(), name='token-login'),
    # - Authenticates users and provides authentication tokens.

    path('token/logout/', CustomDeleteToken.as_view(), name='token-logout'),
    # - Logs out users by deleting their authentication token.

    # JWT Authentication API endpoints
    path('jwt/create/', TokenObtainPairView.as_view(), name='jwt-create'),
    # - Generates JWT access and refresh tokens.

    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    # - Refreshes JWT access tokens.

    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
    # - Verifies a JWT token for authentication.

    # Profile API endpoint
    path('profile/', CustomProfileUserView.as_view(), name='profile'),
    # - Retrieves the authenticated user's profile data.
]
# ======================================================================================================================