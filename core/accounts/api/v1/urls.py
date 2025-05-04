from django.urls import path
from .views import (RegistrationApiView,CustomAuthToken,CustomDeleteToken,
                    CustomChangePasswordView,CustomProfileUserView,SendEmailView)

from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView, TokenVerifyView)

# ======================================================================================================================
app_name = 'api-v1'
urlpatterns = [
    # registeration
    path('registeration/',RegistrationApiView.as_view(),name='register'),


    path('test-email',SendEmailView.as_view(),name='test-email'),

    # change password
    path('change_password/',CustomChangePasswordView.as_view(),name='change_password'),
    # reset password

    # login token
    path('token/login/',CustomAuthToken.as_view(),name='token-login'),
    path('token/logout/',CustomDeleteToken.as_view(),name='token-logout'),
    # login jwt
    path('jwt/create/',TokenObtainPairView.as_view(),name='jwt-create'),
    path('jwt/refresh/',TokenRefreshView.as_view(),name='jwt-refresh'),
    path('jwt/verify/',TokenVerifyView.as_view(),name='jwt-verify'),

    # Profile user
    path('profile/',CustomProfileUserView.as_view(),name='profile'),
]
# ======================================================================================================================