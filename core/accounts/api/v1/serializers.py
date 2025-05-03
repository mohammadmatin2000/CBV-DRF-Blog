from rest_framework import serializers
from ...models import User
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password
# ======================================================================================================================
class UserSerializer(serializers.ModelSerializer):
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
