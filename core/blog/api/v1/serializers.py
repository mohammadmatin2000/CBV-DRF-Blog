from rest_framework import serializers
from ...models import Post

# ======================================================================================================================
# PostSerializer: A serializer class for converting Post model instances into JSON format
class PostSerializer(serializers.ModelSerializer):
    """
    This serializer transforms Post model data into JSON responses for the API.
    """

    class Meta:
        """
        Meta class defines the configuration for the serializer.
        """
        model = Post  # Specifies that this serializer is based on the Post model
        fields = ('id', 'title', 'content', 'status', 'created_date',
                  'updated_date')  # Defines the fields to be included in the API response

# ======================================================================================================================