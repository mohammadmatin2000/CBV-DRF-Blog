from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile


# ======================================================================================================================
# Custom Django Admin Configuration for User model
class CustomUserAdmin(UserAdmin):
    model = (
        User  # Specifies the model that this admin class is based on
    )

    # Defines the fields displayed in the admin panel list view
    list_display = (
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
        "is_verified",
    )

    # Fields used for filtering results in the admin panel
    list_filter = (
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
        "is_verified",
    )

    # Fields used for searching users in the admin panel
    search_fields = ("email",)

    # Orders the results by the email field
    ordering = ("email",)

    # Defines how the user details are grouped and displayed in the admin panel
    fieldsets = (
        (
            "Authentication",
            {  # Section for authentication-related fields
                "fields": ("email", "password")
            },
        ),
        (
            "Permissions",
            {  # Section for managing access control
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "is_verified",
                )
            },
        ),
        (
            "Group Permissions",
            {  # Section for assigning group and user permissions
                "fields": ("groups", "user_permissions")
            },
        ),
        (
            "Important Date",
            {
                "fields": ("last_login",)
            },  # Section for tracking login activity
        ),
    )

    # Configuration for adding a new user from the admin panel
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),  # Styling applied to the form
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",  # Required fields for creating a new user
                    "is_active",
                    "is_superuser",
                ),
            },
        ),
    )


# ======================================================================================================================
# Registers the User model with the custom admin configuration
admin.site.register(User, CustomUserAdmin)

# Registers the Profile model in the admin panel
admin.site.register(Profile)

# ======================================================================================================================
