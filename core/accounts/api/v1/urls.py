from django.urls import path
from .views import RegistrationApiView,CustomAuthToken,CustomDeleteToken

# ======================================================================================================================
app_name = 'api-v1'
urlpatterns = [
    # registeration
    path('registeration/',RegistrationApiView.as_view(),name='register'),
    path('token/login/',CustomAuthToken.as_view(),name='token-login'),
    path('token/logout/',CustomDeleteToken.as_view(),name='token-logout'),
    # change password
    # reset password
    # login token
    # login jwt
]
# ======================================================================================================================