from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError, InvalidSignatureError
from django.conf import settings
from ...models import User, Profile
from .serializers import (
    CustomRegistrationApiView, CustomAuthTokenSerializer, CustomChangePasswordSerializer,
    CustomProfileUser, CustomActivationResendSerializer, CustomResetPasswordSerializer
)
from ..utils import EmailThread
# ======================================================================================================================
# RegistrationApiView: Handles user registration and sends an activation email
class RegistrationApiView(generics.GenericAPIView):
    """
    This API view allows users to register their accounts.
    """

    queryset = User.objects.all()  # Retrieves all users
    serializer_class = CustomRegistrationApiView  # Uses a serializer for validation and user creation

    def post(self, request, *args, **kwargs):
        """
        Handles user registration via POST request.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.data['email']
            user_obj = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_obj)

            # Sending activation email
            email_obj = EmailMessage(
                'email/activation.tpl', {'token': token}, 'matin20001313@gmail.com', to=[email]
            )
            EmailThread(email_obj).start()

            return Response({'email': email}, status=status.HTTP_201_CREATED)

    def get_tokens_for_user(self, user):
        """
        Generates a JWT access token for the user.
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
# ======================================================================================================================
# CustomAuthToken: Handles user authentication and token generation
class CustomAuthToken(ObtainAuthToken):
    """
    This view authenticates a user and returns an authentication token.
    """

    serializer_class = CustomAuthTokenSerializer  # Uses CustomAuthTokenSerializer for authentication

    def post(self, request, *args, **kwargs):
        """
        Authenticates a user and generates a token.
        """
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
# ======================================================================================================================
# CustomDeleteToken: Logs out the user by deleting their authentication token
class CustomDeleteToken(APIView):
    """
    This view deletes the user's authentication token, effectively logging them out.
    """

    permission_classes = (IsAuthenticated,)  # Requires authentication

    def post(self, request):
        """
        Deletes the user's authentication token.
        """
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# ======================================================================================================================
# CustomChangePasswordView: Handles password change requests
class CustomChangePasswordView(generics.GenericAPIView):
    """
    This API view allows authenticated users to change their password.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = CustomChangePasswordSerializer

    def get_object(self):
        """
        Returns the authenticated user object.
        """
        return self.request.user

    def put(self, request, *args, **kwargs):
        """
        Handles password updates via PUT request.
        """
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.validated_data.get("old_password")):
                return Response({"old_password": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data["new_password"])
            user.save()

            return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ======================================================================================================================
# CustomResetPasswordView: Handles password reset requests via email
class CustomResetPasswordView(generics.GenericAPIView):
    """
    This API view allows users to reset their password by providing their email.
    """

    serializer_class = CustomResetPasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handles password resets via POST request.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        new_password = serializer.validated_data['new_password']

        user = get_object_or_404(User, email=email)
        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password reset successfully."}, status=status.HTTP_200_OK)
# ======================================================================================================================
# CustomProfileUserView: Retrieves authenticated user's profile information
class CustomProfileUserView(generics.GenericAPIView):
    """
    This API view allows authenticated users to retrieve their profile information.
    """

    queryset = Profile.objects.all()
    serializer_class = CustomProfileUser
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """
        Retrieves the authenticated user's profile.
        """
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj
# ======================================================================================================================
# CustomActivationView: Handles account activation via token verification
class CustomActivationView(APIView):
    """
    This API view verifies a user's activation token and activates their account.
    """

    def get(self, request, token, *args, **kwargs):
        """
        Decodes the activation token and verifies the user.
        """
        try:
            decode = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])  # Decodes the token
            user_id = decode['user_id']
        except ExpiredSignatureError:
            return Response({"detail": "Token has expired"}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidSignatureError:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        user_obj = get_object_or_404(User, id=user_id)

        if not user_obj.is_verified:
            user_obj.is_verified = True
            user_obj.save()
            return Response({"detail": "Verified"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Already verified"}, status=status.HTTP_400_BAD_REQUEST)
# ======================================================================================================================
# CustomActivationResendView: Resends activation email
class CustomActivationResendView(generics.GenericAPIView):
    """
    This API view resends the account activation email.
    """

    serializer_class = CustomActivationResendSerializer  # Uses CustomActivationResendSerializer for validation

    def post(self, request, *args, **kwargs):
        """
        Handles activation email resending via POST request.
        """
        serializer_class = CustomActivationResendSerializer(data=request.data)
        if serializer_class.is_valid():
            user_obj = serializer_class.validated_data['user']
            token = self.get_tokens_for_user(user_obj)

            email_obj = EmailMessage(
                'email/activation.tpl', {'token': token}, 'matin20001313@gmail.com', to=[user_obj.email]
            )
            EmailThread(email_obj).start()

            return Response({'detail': 'Email sent successfully'}, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        """
        Generates an authentication token for the user.
        """
        refresh = RefreshToken.for_user(user)
        return {'token': str(refresh.access_token)}
# ======================================================================================================================