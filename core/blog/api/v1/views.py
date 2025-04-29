from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer
from ...models import Post

# ======================================================================================================================
# `api_view()` decorator converts this function-based view into an API endpoint
@api_view()
def post_listview(request):
    """
    API endpoint to retrieve a list of published posts.
    """
    posts = Post.objects.filter(status=1)  # Filters only posts with status=1 (published posts)
    serializer = PostSerializer(posts, many=True)  # Serializes the queryset to JSON format
    return Response(serializer.data)  # Returns JSON response containing serialized post data
# ======================================================================================================================
# `api_view()` decorator makes this function an API endpoint for retrieving a single post by ID
@api_view()
def post_detailview(request, id):
    """
    API endpoint to retrieve details of a specific post by its ID.
    """
    try:
        post = Post.objects.get(id=id, status=1)  # Fetches the post with the given ID and status=1 (published)
        serializer = PostSerializer(post)  # Serializes the single post instance
        return Response(serializer.data)  # Returns JSON response with post data

    except Post.DoesNotExist:  # Handles the case where the requested post doesn't exist
        return Response({"detail": "Post Does Not Exist"}, status=status.HTTP_404_NOT_FOUND)  # Returns a 404 error
# ======================================================================================================================