from pathlib import Path
from decouple import config

# ======================================================================================================================
# Setting up base directory paths
BASE_DIR = Path(__file__).resolve().parent.parent

# ======================================================================================================================
# Security settings

# SECRET_KEY: Stores the secret key securely using environment variables (do not expose in production)
SECRET_KEY = config("SECRET_KEY",default="test")

# DEBUG: Determines whether the application runs in debug mode (False in production)
DEBUG = config("DEBUG", default=True, cast=bool)

# ALLOWED_HOSTS: Defines the list of host/domain names allowed to access the application
ALLOWED_HOSTS = ["*"]


# ======================================================================================================================
# Installed Applications: Defines Django's built-in and third-party apps

INSTALLED_APPS = [
    "django.contrib.admin",  # Django Admin Panel
    "django.contrib.auth",  # Authentication System
    "django.contrib.contenttypes",  # Content Types Framework
    "django.contrib.sessions",  # Session Management
    "django.contrib.messages",  # Messaging Framework
    "django.contrib.staticfiles",  # Static File Management
    # Custom apps
    "accounts",
    "blog",
    # Third-party apps
    "rest_framework",  # Django REST Framework for API development
    "rest_framework.authtoken",  # Token-based authentication
    "rest_framework_simplejwt",  # JWT authentication support
    "django_filters",  # Filtering support for querysets
    "drf_yasg",  # OpenAPI (Swagger) documentation generator
    "mail_templated",  # Email templating system
    "djoser",  # Authentication and user management API
    "corsheaders",
    "django_celery_beat",
]

# ======================================================================================================================
# Middleware: Defines request handling layers

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # Improves security features
    "django.contrib.sessions.middleware.SessionMiddleware",  # Manages session data
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",  # Handles common request/response operations
    "django.middleware.csrf.CsrfViewMiddleware",  # Protects against CSRF attacks
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Manages user authentication
    "django.contrib.messages.middleware.MessageMiddleware",  # Handles messaging framework
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Protects against clickjacking attacks
]

# ======================================================================================================================
# URL Configuration

ROOT_URLCONF = "core.urls"

# ======================================================================================================================
# Template Configuration: Defines template engines and context processors

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",  # Django template engine
        "DIRS": [
            BASE_DIR / "templates"
        ],  # Specifies the template directory
        "APP_DIRS": True,  # Enables automatic template discovery in installed apps
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",  # Debugging context processor
                "django.template.context_processors.request",  # Request-based context processor
                "django.contrib.auth.context_processors.auth",  # Authentication-related context processor
                "django.contrib.messages.context_processors.messages",  # Messaging framework context processor
            ],
        },
    },
]

# ======================================================================================================================
# WSGI Configuration (Web Server Gateway Interface)
WSGI_APPLICATION = "core.wsgi.application"

# ======================================================================================================================
# Database Configuration

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",  # SQLite database engine (replace with PostgreSQL/MySQL for production)
        "NAME": BASE_DIR / "db.sqlite3",  # Database file location
    }
}

# ======================================================================================================================
# Password Validation: Enforces strong password policies

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },  # Prevents similar passwords
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"
    },  # Enforces minimum length
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
    },  # Prevents common passwords
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },  # Restricts fully numeric passwords
]

# ======================================================================================================================
# Localization & Timezone Settings

LANGUAGE_CODE = "en-us"  # Defines the default language (English - US)
TIME_ZONE = "UTC"  # Defines the default timezone (UTC)
USE_I18N = True  # Enables internationalization support
USE_TZ = True  # Enables timezone-aware datetime handling

# ======================================================================================================================
# Static & Media File Management

STATIC_URL = "/static/"  # Defines the URL for static files
STATIC_ROOT = (
    BASE_DIR / "static"
)  # Specifies the directory for collected static files

MEDIA_URL = "/media/"  # Defines the URL for media files
MEDIA_ROOT = (
    BASE_DIR / "media"
)  # Specifies the directory for uploaded media files

STATICFILES_DIRS = [
    BASE_DIR
    / "staticfiles",  # Defines additional static file directories
]

# ======================================================================================================================
# Primary Key Field Type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"  # Uses BigAutoField as the default primary key type

# ======================================================================================================================
# Custom User Model Configuration

AUTH_USER_MODEL = "accounts.User"  # Defines a custom user model (instead of Django's default user model)

# ======================================================================================================================
# Django REST Framework Configuration

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",  # Defines schema class for API documentation
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",  # Basic authentication
        "rest_framework.authentication.SessionAuthentication",  # Session-based authentication
        "rest_framework.authentication.TokenAuthentication",  # Token-based authentication
        "rest_framework_simplejwt.authentication.JWTAuthentication",  # JWT authentication
    ],
}

# ======================================================================================================================
# Email Configuration

# EMAIL_BACKEND: Defines the email backend used for sending emails
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# SMTP Configuration
EMAIL_HOST = "smtp4dev"  # Defines the SMTP email server
EMAIL_PORT = 25  # Defines the SMTP port
EMAIL_HOST_USER = (
    ""  # Defines SMTP authentication username (if applicable)
)
EMAIL_HOST_PASSWORD = (
    ""  # Defines SMTP authentication password (if applicable)
)
EMAIL_USE_TLS = False  # Determines whether TLS security is used

# ======================================================================================================================
CORS_ALLOWED_ORIGINS = True



# ======================================================================================================================

CELERY_BROKER_URL = "redis://redis:6379/0"

# ======================================================================================================================
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}# ======================================================================================================================
