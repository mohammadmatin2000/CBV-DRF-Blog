from rest_framework import generics
from .serializers import CustomRegistrationApiView, CustomAuthTokenSerializer, CustomChangePasswordSerializer, \
    CustomProfileUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from ...models import User, Profile
from mail_templated import EmailMessage
from ..utils import EmailThread
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from jwt.exceptions import DecodeError,ExpiredSignatureError,InvalidSignatureError
from django.conf import settings


# ======================================================================================================================
class RegistrationApiView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = CustomRegistrationApiView

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.data['email']
            data = {
                'email': email,
            }
            user_obj = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage('email/activation.tpl', {'token': token}, 'matin20001313@gmail.com'
                                     , to=[email])
            EmailThread(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


# ======================================================================================================================
class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


# ======================================================================================================================
class CustomDeleteToken(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ======================================================================================================================
class CustomChangePasswordView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
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
class CustomProfileUserView(generics.GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = CustomProfileUser
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


# ======================================================================================================================
class SendEmailView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        self.email = 'naderghorbanpur@gmail.com'
        user_obj = get_object_or_404(User, email=self.email)
        token = self.get_tokens_for_user(user_obj)

        email_obj = EmailMessage('email/hello.tpl', {'token': token}, 'matin20001313@gmail.com'
                                 , to=[self.email])

        # TODO: Add more useful commands here.
        EmailThread(email_obj).start()
        return Response("test ok")

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {'token': str(refresh.access_token)}


# ======================================================================================================================
class CustomActivationView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            decode = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
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
            return Response({"detail": "Not verified"}, status=status.HTTP_400_BAD_REQUEST)
# ======================================================================================================================
class CustomActivationResendView(APIView):
    pass