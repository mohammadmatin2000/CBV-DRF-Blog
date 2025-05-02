from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from .serializers import PostSerializer, CategorySerializer
from ...models import Post, Category
from rest_framework import viewsets
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from .paginations import DefaultPagination
# ======================================================================================================================
# PostModelViewSet: A ViewSet for managing Post objects via the REST API
class PostModelViewSet(viewsets.ModelViewSet):
    """
    This ViewSet handles CRUD operations for published posts.
    """
    queryset = Post.objects.filter(status=1)  # Retrieves only posts marked as published (status=1)
    serializer_class = PostSerializer  # Uses PostSerializer to convert model instances into JSON format
    permission_classes = (IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)  # Allows authenticated users to modify posts, while others can only read
    filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter)
    filterset_fields = {
        "category":["exact","in"],
        "author":["exact"],
        "status": ["exact"],
    }
    search_fields = ['title','content']
    ordering_fields = ['published_date']
    pagination_class = DefaultPagination
# ======================================================================================================================
# CategoryModelViewSet: A ViewSet for managing Category objects via the REST API
class CategoryModelViewSet(viewsets.ModelViewSet):
    """
    This ViewSet handles CRUD operations for categories.
    """
    queryset = Category.objects.all()  # Retrieves all category objects from the database
    serializer_class = CategorySerializer  # Uses CategorySerializer to serialize category data
    permission_classes = (IsAuthenticatedOrReadOnly,)  # Allows authenticated users to modify categories, while others can only read

# ======================================================================================================================