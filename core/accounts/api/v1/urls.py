from django.urls import path
from .views import RegistrationApiView
# ======================================================================================================================
app_name = 'api-v1'
urlpatterns = [
    # registeration
    path('registeration/',RegistrationApiView.as_view(),name='register'),
    # change password
    # reset password
    # login token
    # login jwt
]
# ======================================================================================================================