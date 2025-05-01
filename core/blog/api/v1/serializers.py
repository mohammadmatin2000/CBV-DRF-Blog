from rest_framework import serializers
from ...models import Post, Category


# ======================================================================================================================
# PostSerializer: A serializer class for converting Post model instances into JSON format
class PostSerializer(serializers.ModelSerializer):
    """
    This serializer transforms Post model data into JSON responses for the API.
    """

    snippet = serializers.ReadOnlyField(source='get_snippet')  # Retrieves a brief snippet of the post content
    relative_url = serializers.URLField(source='get_absolute_api_url')  # Stores the relative API URL for the post
    absolute_url = serializers.SerializerMethodField()  # Defines a method field for absolute URL generation

    class Meta:
        """
        Meta class defines the configuration for the serializer.
        """
        model = Post  # Specifies that this serializer is based on the Post model
        fields = ('id', 'title', 'content', 'status', 'created_date',
                  'updated_date', 'author', 'snippet', 'relative_url',
                  'absolute_url')  # Defines the fields to be included in the API response
        read_only_fields = (
        'created_date', 'updated_date')  # Specifies that created_date and updated_date should not be modified

    def get_absolute_url(self, obj):
        """
        This method generates the absolute URL for the post using the request context.
        """
        return self.context.get('request').build_absolute_uri(obj.pk)


# ======================================================================================================================
# CategorySerializer: A serializer class for converting Category model instances into JSON format
class CategorySerializer(serializers.ModelSerializer):
    """
    This serializer transforms Category model data into JSON responses for the API.
    """

    class Meta:
        """
        Meta class defines the configuration for the serializer.
        """
        model = Category  # Specifies that this serializer is based on the Category model
        fields = ('id', 'name')  # Defines the fields to be included in the API response

# ======================================================================================================================