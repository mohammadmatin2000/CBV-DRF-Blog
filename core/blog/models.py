from django.db import models
# from django.contrib.auth import get_user_model

# Getting the user model object dynamically
# User = get_user_model()

# ======================================================================================================================
class Post(models.Model):
    """
    This class defines the Post model for the blog application.
    """

    image = models.ImageField(null=True, blank=True)  # Optional image field for the post
    author = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)  # References the user who created the post
    title = models.CharField(max_length=255)  # Stores the post title with a max length of 255 characters
    content = models.TextField()  # Stores the post content as a text field
    category = models.ForeignKey('Category', on_delete=models.CASCADE)  # Links the post to a category
    status = models.BooleanField(default=False)  # Determines whether the post is published (True) or draft (False)
    published_date = models.DateTimeField(auto_now_add=True)  # Automatically sets the published date upon creation
    created_date = models.DateTimeField(auto_now_add=True)  # Automatically sets the creation date
    updated_date = models.DateTimeField(auto_now=True)  # Automatically updates the date whenever the post is modified

    def __str__(self):
        return self.title  # Returns the post title when printing the object

# ======================================================================================================================
class Category(models.Model):
    """
    This class defines the Category model, which categorizes blog posts.
    """

    name = models.CharField(max_length=255)  # Stores the category name with a max length of 255 characters

    def __str__(self):
        return self.name  # Returns the category name when printing the object

# ======================================================================================================================