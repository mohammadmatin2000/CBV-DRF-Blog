from rest_framework import generics
from .serializers import UserSerializer,CustomAuthTokenSerializer
from ...models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# ======================================================================================================================
class RegistrationApiView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
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