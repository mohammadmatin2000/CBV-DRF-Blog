from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import HttpResponse
# ======================================================================================================================
# API Documentation Configuration using drf-yasg (Yet Another Swagger Generator)
schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",  # API title displayed in Swagger UI
        default_version="v1",  # API version
        description="Test description",  # Description of the API
        terms_of_service="https://www.google.com/policies/terms/",  # Terms of service link
        contact=openapi.Contact(
            email="contact@snippets.local"
        ),  # Contact email for API support
        license=openapi.License(
            name="BSD License"
        ),  # API license information
    ),
    public=True,  # Makes the API documentation publicly accessible
    permission_classes=(
        permissions.AllowAny,
    ),  # Grants access to any user without authentication
)
def index(request):
    return HttpResponse("<h1>Home Page</h1>")
# ======================================================================================================================
# Defining URL patterns for the Django application
urlpatterns = [
    # Django Admin Panel - Backend management system
    path("admin/", admin.site.urls),
    # Blog application URLs
    path("", include("blog.urls")),
    path("",index,name="index"),
    # User Authentication & Account Management
    path("accounts/", include("accounts.urls")),
    # Django REST framework built-in authentication views (login, logout, etc.)
    path("api-auth/", include("rest_framework.urls")),
    # API Documentation using Django REST Framework's built-in docs
    path("api-docs/", include_docs_urls(title="API Sample")),
    # API documentation routes using Swagger and ReDoc
    path(
        "swagge/output.json/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),  # JSON schema output
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),  # Swagger UI
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),  # ReDoc UI
]
# ======================================================================================================================
# Serving media and static files in development mode
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )  # Handles media files
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )  # Handles static files

# ======================================================================================================================
