from django.contrib import admin
from .models import Post, Category

# ======================================================================================================================
# Custom Django Admin Configuration for managing Post and Category models
class PostAdmin(admin.ModelAdmin):
    """
    This class customizes the Django admin interface for the Post model.
    """

    # Defines the fields displayed in the admin panel list view for posts
    list_display = ('title', 'author', 'category', 'status', 'created_date', 'published_date')

    # Enables filtering posts by their status in the admin panel
    list_filter = ('status',)

    # Allows admin users to search for posts by title
    search_fields = ('title',)

# Registers the Post model with the custom admin configuration
admin.site.register(Post, PostAdmin)

# Registers the Category model in the admin panel with default settings
admin.site.register(Category)

# ======================================================================================================================