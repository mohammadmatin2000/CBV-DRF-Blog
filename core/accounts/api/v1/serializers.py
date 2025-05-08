from rest_framework import serializers
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from ...models import User, Profile


# ======================================================================================================================
# CustomRegistrationApiView: Handles user registration with password validation
class CustomRegistrationApiView(serializers.ModelSerializer):
    """
    Serializer for user registration, including password confirmation and validation.
    """

    password1 = serializers.CharField(
        max_length=255, write_only=True
    )  # Secondary password field for confirmation

    class Meta:
        """
        Meta configuration for the serializer.
        """

        model = User  # Defines the associated model (User)
        fields = (
            "email",
            "password",
            "password1",
        )  # Specifies the fields included in API response
        extra_kwargs = {
            "password": {
                "write_only": True
            },  # Ensures password field is write-only for security
        }

    def validate(self, data):
        """
        Validates that the passwords match and comply with Django's password strength requirements.
        """
        if data.get("password") != data.get("password1"):
            raise serializers.ValidationError(
                {"detail": "Passwords must match"}
            )  # Ensures passwords are identical

        try:
            validate_password(
                data.get("password")
            )  # Runs Django's built-in password validation checks
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {"password": e.messages}
            )  # Raises validation errors if password is weak

        return data

    def create(self, validated_data):
        """
        Creates a new user after removing the password confirmation field.
        """
        validated_data.pop(
            "password1"
        )  # Removes the confirmation field before user creation
        password = validated_data.pop(
            "password"
        )  # Extracts the password
        user = User(**validated_data)  # Creates a new user instance
        user.set_password(
            password
        )  # Hashes and sets the password securely
        user.save()  # Saves the user instance in the database
        return user


# ======================================================================================================================
# CustomAuthTokenSerializer: Handles user authentication and token generation
class CustomAuthTokenSerializer(serializers.Serializer):
    """
    Serializer for user authentication via email and password.
    """

    email = serializers.CharField(
        label=_("Email"), write_only=True
    )  # Email field
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )  # Password field
    token = serializers.CharField(
        label=_("Token"), read_only=True
    )  # Token field (typically used for authentication response)

    def validate(self, attrs):
        """
        Authenticates user credentials and checks account verification status.
        """
        username = attrs.get("email")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )  # Authenticates user

            if not user:  # If authentication fails, return an error
                raise serializers.ValidationError(
                    _("Unable to log in with provided credentials."),
                    code="authorization",
                )
            if not getattr(
                user, "is_verified", False
            ):  # Ensures user account is verified before allowing login
                raise serializers.ValidationError(
                    {"detail": "User account is not verified."}
                )
        else:
            raise serializers.ValidationError(
                _('Must include "username" and "password".'),
                code="authorization",
            )

        attrs["user"] = user  # Adds authenticated user to attributes
        return attrs


# ======================================================================================================================
# CustomChangePasswordSerializer: Handles password change requests
class CustomChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing user passwords securely.
    """

    old_password = serializers.CharField(
        write_only=True
    )  # Old password field
    new_password = serializers.CharField(
        write_only=True
    )  # New password field
    new_password_confirmation = serializers.CharField(
        write_only=True
    )  # Confirmation for the new password

    def validate(self, attrs):
        """
        Ensures the new passwords match and are strong.
        """
        if attrs.get("new_password") != attrs.get(
            "new_password_confirmation"
        ):
            raise serializers.ValidationError(
                {"detail": "Passwords must match"}
            )  # Ensures passwords match

        try:
            validate_password(
                attrs.get("new_password")
            )  # Runs password strength validation
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {"new_password": e.messages}
            )  # Raises validation errors if password is weak

        return attrs


# ======================================================================================================================
# CustomResetPasswordSerializer: Handles password reset requests
class CustomResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for resetting a user's password using their email.
    """

    email = serializers.EmailField()  # User's email field
    new_password = serializers.CharField(
        write_only=True, min_length=8, required=True
    )  # New password field

    def validate_new_password(self, value):
        """
        Validates the new password using Django's built-in password rules.
        """
        validate_password(value)  # Runs password strength validation
        return value

    def validate(self, data):
        """
        Ensures the email belongs to an existing user.
        """
        email = data.get("email")
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "No user associated with this email."
            )  # Prevents resetting passwords for non-existent users
        return data

    def save(self):
        """
        Updates the user's password after validation.
        """
        email = self.validated_data["email"]
        new_password = self.validated_data["new_password"]

        user = User.objects.get(email=email)
        user.set_password(new_password)  # Securely updates password
        user.save()

        return user


# ======================================================================================================================
# CustomProfileUser: Handles user profile serialization
class CustomProfileUser(serializers.ModelSerializer):
    """
    Serializer for retrieving user profile details.
    """

    email = serializers.CharField(
        source="user.email", read_only=True
    )  # Displays email from the associated user model

    class Meta:
        """
        Meta configuration for the serializer.
        """

        model = Profile  # Specifies the associated Profile model
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "image",
            "designation",
        )  # Specifies the fields included in API response


# ======================================================================================================================
# CustomActivationResendSerializer: Handles resending account activation emails
class CustomActivationResendSerializer(serializers.Serializer):
    """
    Serializer for resending account activation emails to users who have not yet verified their accounts.
    """

    email = serializers.CharField(required=True)  # Email field

    def validate(self, attrs):
        """
        Checks if the user exists and whether their account is already verified.
        """
        email = attrs.get("email")
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": _("User does not exist.")}
            )  # Ensures user exists

        attrs["user"] = user_obj  # Stores user data in attributes

        if user_obj.is_verified:
            raise serializers.ValidationError(
                {"detail": "User account is already verified."}
            )  # Prevents resending activation to verified users

        return attrs


# ======================================================================================================================
