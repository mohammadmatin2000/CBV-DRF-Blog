from django.urls import path, include  # Importing path and include for routing URLs
from .views import send_email, test  # Importing view functions for specific endpoints
from .views import weather_view  # Importing the weather view

# ======================================================================================================================
# Setting the application namespace for URL reversibility and organization
app_name = "accounts"

# Defining URL patterns for authentication and API endpoints
urlpatterns = [
    # Includes Django's built-in authentication URLs (login, logout, password management)
    path("", include("django.contrib.auth.urls")),

    # Includes API version 1 authentication and account-related routes
    path("api/v1/", include("accounts.api.v1.urls")),

    # Email sending endpoint (mapped to send_email function)
    path('send_email/', send_email, name='sendemail'),

    # Test endpoint (mapped to test function)
    path("test/", test, name="test"),

    # Weather API endpoint (mapped to weather_view function)
    path('api/weather/', weather_view, name='weather'),

    # API version 2 authentication system (Djoser - commented out for now)
    # path('api/v2/', include('djoser.urls')),

    # JWT authentication system (Djoser - commented out for now)
    # path('api/v2/', include('djoser.urls.jwt')),
]

# ======================================================================================================================