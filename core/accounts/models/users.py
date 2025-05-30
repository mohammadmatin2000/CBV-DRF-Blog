from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _


# ======================================================================================================================
# Custom user model manager where email is the unique identifier instead of usernames
class UserManager(BaseUserManager):
    """
    This custom user manager class defines how users and superusers are created.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a regular user with the given email and password.
        """
        if not email:
            raise ValueError(
                _("The Email must be set")
            )  # Ensures email is provided
        email = self.normalize_email(
            email
        )  # Normalizes the email format
        user = self.model(
            email=email, **extra_fields
        )  # Creates a new user instance
        user.set_password(password)  # Hashes and sets the password
        user.save()  # Saves the user instance in the database
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a SuperUser with the given email and password.
        """
        extra_fields.setdefault(
            "is_staff", True
        )  # Superuser must be staff
        extra_fields.setdefault(
            "is_superuser", True
        )  # Superuser must have all privileges
        extra_fields.setdefault(
            "is_active", True
        )  # Superuser is active by default
        extra_fields.setdefault("is_verified", True)

        # Validation to ensure superuser properties are properly assigned
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            email, password, **extra_fields
        )  # Calls create_user method


# ======================================================================================================================
# Custom User Model extending Django's AbstractBaseUser and PermissionsMixin
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model for authentication, using email as the primary identifier.
    """

    email = models.EmailField(
        max_length=255, unique=True
    )  # Unique email field
    is_staff = models.BooleanField(
        default=False
    )  # Determines staff/admin access
    is_active = models.BooleanField(
        default=True
    )  # Indicates whether the account is active
    is_verified = models.BooleanField(
        default=False
    )  # Optional field for email verification

    USERNAME_FIELD = (
        "email"  # Defines email as the login username field
    )
    REQUIRED_FIELDS = (
        []
    )  # No additional required fields besides email and password

    created_date = models.DateTimeField(
        auto_now_add=True
    )  # Automatically sets creation time
    updated_date = models.DateTimeField(
        auto_now=True
    )  # Updates timestamp on modification

    objects = (
        UserManager()
    )  # Assigns the custom UserManager for user management

    def __str__(self):
        return (
            self.email
        )  # Returns email as the string representation of the user object


# ======================================================================================================================
