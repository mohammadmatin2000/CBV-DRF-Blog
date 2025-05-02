# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
# from .serializers import PostSerializer
# from ...models import Post
# from rest_framework.generics import GenericAPIView,ListAPIView,ListCreateAPIView
# from rest_framework import mixins
# from rest_framework.views import APIView
# from django.shortcuts import get_object_or_404
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView


# ======================================================================================================================
# @api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
# def post_listview(request):
#     """
#     API endpoint to retrieve a list of published posts.
#     """
#     if request.method == 'GET':
#         posts = Post.objects.filter(status=1)  # Filters only posts with status=1 (published posts)
#         serializer = PostSerializer(posts, many=True)  # Serializes the queryset to JSON format
#         return Response(serializer.data)  # Returns JSON response containing serialized post data
#     elif request.method == 'POST':
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ======================================================================================================================
# `api_view()` decorator makes this function an API endpoint for retrieving a single post by ID
# @api_view(['GET', 'PUT', 'DELETE'])
# def post_detailview(request, id):
#     """
#     API endpoint to retrieve details of a specific post by its ID.
#     """
#     post = Post.objects.get(id=id, status=1)
#     if request.method == 'GET':
#           # Fetches the post with the given ID and status=1 (published)
#         serializer = PostSerializer(post)  # Serializes the single post instance
#         return Response(serializer.data)  # Returns JSON response with post data
#     elif request.method == 'PUT':
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         post.delete()
#         return Response({"detail":"Item Removed Successfully"},status=status.HTTP_204_NO_CONTENT)
# ======================================================================================================================
# class PostList(GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     serializer_class = PostSerializer
#     queryset = Post.objects.filter(status=1)
#     def get(self,request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
# ======================================================================================================================
# class PostDetail(APIView):
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     serializer_class = PostSerializer
#     def get(self, request, id):
#         post = get_object_or_404(Post, id=id)
#         serializer = self.serializer_class(post)
#         return Response(serializer.data)
#     def put(self, request, id):
#         post = get_object_or_404(Post, id=id)
#         serializer = self.serializer_class(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     def delete(self, request, id):
#         post = get_object_or_404(Post, id=id)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# ======================================================================================================================
# class PostDetail(GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     serializer_class = PostSerializer
#     queryset = Post.objects.filter(status=1)
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
# ======================================================================================================================
# class PostList(ListCreateAPIView):
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     serializer_class = PostSerializer
#     queryset = Post.objects.filter(status=1)
# ======================================================================================================================
# class PostDetail(RetrieveUpdateDestroyAPIView):
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     serializer_class = PostSerializer
#     queryset = Post.objects.filter(status=1)
# ======================================================================================================================
# class PostViewSet(viewsets.ViewSet):
#     queryset = Post.objects.filter(status=1)
#     serializer_class = PostSerializer
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     def list(self, request):
#         queryset = self.queryset.filter(status=1)
#         serializer = PostSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     # ==================================================================================================================
#     def create(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)
#
#     # ==================================================================================================================
#     def retrieve(self, request, pk=None):
#         post = get_object_or_404(self.queryset, pk=pk)
#         serializer = self.serializer_class(post)
#         return Response(serializer.data)
#
#     # ==================================================================================================================
#     def update(self, request, pk=None):
#         post_object=get_object_or_404(self.queryset, pk=pk)
#         serializer = self.serializer_class(post_object, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     # ==================================================================================================================
#     def destroy(self, request, pk=None):
#         post_object=get_object_or_404(self.queryset, pk=pk)
#         post_object.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#     # ==================================================================================================================
#     def partial_update(self, request, pk=None):
#         pass
# ======================================================================================================================
# Defining URL patterns for the API endpoints
# urlpatterns = [
#     Maps '/post/' to the post_listview function, returning a list of all published posts
#     path('post/', post_listview, name='post_list'),
#     Maps '/post/<int:id>/' to the post_detailview function, retrieving a specific post by its ID
#     path('post/<int:id>/', post_detailview, name='post_detail'),
#     path('post/', PostList.as_view(), name='post-list'),
#     path('post/<int:pk>/', PostDetail.as_view(), name='post-detail'),
#     path('post/',PostViewSet.as_view({'get':'list','post':'create'}),name='post-list'),
#     path('post/<int:pk>',PostViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'}),name='post-list'),
# ]
# ======================================================================================================================