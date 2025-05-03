from rest_framework import generics
from .serializers import UserSerializer
from ...models import User
from rest_framework.response import Response
from rest_framework import status

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