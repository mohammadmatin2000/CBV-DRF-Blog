from django.forms import ModelForm
from .models import Post

# ======================================================================================================================
# This class defines a ModelForm for the Post model
class PostForm(ModelForm):
    class Meta:
        """
        Meta class defines the configuration for the ModelForm.
        """
        model = Post  # Specifies that this form is based on the Post model
        fields = ['title', 'content', 'category', 'status']  # Defines which fields are included in the form

# ======================================================================================================================