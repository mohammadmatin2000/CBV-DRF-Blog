from rest_framework import generics
from .serializers import CustomRegistrationApiView,CustomAuthTokenSerializer,CustomChangePasswordSerializer,CustomProfileUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from ...models import User,Profile
from django.core.mail import send_mail

# ======================================================================================================================
class RegistrationApiView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = CustomRegistrationApiView
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data={
                'email': serializer.data['email'],
            }
            return Response(data, status=status.HTTP_201_CREATED)
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
        obj= get_object_or_404(queryset, user=self.request.user)
        return obj
# ======================================================================================================================
class SendEmailView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        send_mail(
            "Subject here",
            "Here is the message.",
            "from@example.com",
            ["to@example.com"],
            fail_silently=False,
        )
        return Response("test ok")
# ======================================================================================================================
