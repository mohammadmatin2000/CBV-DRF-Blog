from rest_framework import serializers
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from ...models import User,Profile
# ======================================================================================================================
class CustomRegistrationApiView(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password1')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data.get('password') != data.get('password1'):
            raise serializers.ValidationError({'detail': 'Passwords must match'})

        try:
            validate_password(data.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})
        return data

    def create(self, validated_data):
        validated_data.pop('password1')  # Remove password1 to avoid TypeError
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
# ======================================================================================================================
class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            if not getattr(user, "is_verified", False):  # ✅ Avoid direct attribute access
                raise serializers.ValidationError({"detail": "User account is not verified."})
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
# ======================================================================================================================
class CustomChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    new_password_confirmation = serializers.CharField(write_only=True)
    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('new_password_confirmation'):
            raise serializers.ValidationError({'detail': 'Passwords must match'})
        try:
            validate_password(attrs.get('new_password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'new_password': e.messages})
        return attrs
# ======================================================================================================================
class CustomProfileUser(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)
    class Meta:
        model = Profile
        fields = ('id','email','first_name','last_name','image','designation')
# ======================================================================================================================