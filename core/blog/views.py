from django.views.generic import (
    TemplateView,
    RedirectView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.views.generic import ListView
from .models import Post
from .forms import PostForm


# ======================================================================================================================
# IndexView: A template-based view that renders the 'index.html' page
class IndexView(TemplateView):
    template_name = (
        "index.html"  # Specifies which template should be used
    )

    def get_context_data(self, **kwargs):
        """
        This method adds extra context data to the template.
        """
        context = super().get_context_data(
            **kwargs
        )  # Gets the default context
        context["title"] = "Blog"  # Adds a title to the context
        context["posts"] = (
            Post.objects.all()
        )  # Fetches all blog posts
        return context


# ======================================================================================================================
# RedirectToMakt: A redirect view that directs users to an external website
class RedirectToMakt(RedirectView):
    url = "https://maktabkhooneh.com/"  # Redirects users to this URL


# ======================================================================================================================
# PostListView: A class-based view to display a paginated list of posts
class PostListView(
    PermissionRequiredMixin, LoginRequiredMixin, ListView
):
    permission_required = "blog.view_post"
    model = Post  # Specifies the model to retrieve objects from
    context_object_name = (
        "posts"  # Assigns a name to the list of posts in the template
    )
    paginate_by = 4  # Limits the number of posts displayed per page
    ordering = "id"  # Orders posts by their ID (ascending order)

    # Uncommented version could be used to filter only published posts
    # queryset = Post.objects.all()
    # def get_queryset(self):
    #     return Post.objects.filter(status=1)


# ======================================================================================================================
# PostDetailView: A class-based view to display the details of a single post
class PostDetailView(LoginRequiredMixin, DetailView):
    model = (
        Post  # Specifies the model to retrieve a single post instance
    )


# ======================================================================================================================
# PostFormView: A class-based view for handling post creation using Django's CreateView
class PostFormView(LoginRequiredMixin, CreateView):
    model = Post  # Specifies the model the form interacts with
    form_class = (
        PostForm  # Defines the form class used to create a post
    )
    success_url = "/postlist/"  # Redirects to the post list page after successful form submission

    def form_valid(self, form):
        """
        Overwrites the form_valid method to assign the logged-in user as the author.
        """
        form.instance.author = (
            self.request.user
        )  # Sets the author to the currently logged-in user
        return super().form_valid(
            form
        )  # Calls the parent method to complete form submission

    # Alternative approach: Fields could be explicitly listed instead of using a form class
    # fields = ['title', 'content','category','status']


# ======================================================================================================================
"""
Alternative PostFormView using FormView instead of CreateView:
class PostFormView(FormView):
    template_name = "contact.html"  # Specifies the template used for displaying the form
    form_class = PostForm  # Defines the form class for post submission
    success_url = "/postlist/"  # Redirects to post list on successful form submission

    def form_valid(self, form):
        form.save()  # Saves the form instance
        return super().form_valid(form)
"""


# ======================================================================================================================
# PostUpdateView: A class-based view to handle updating an existing post
class PostUpdateView(LoginRequiredMixin, UpdateView):
    """
    This view allows authenticated users to update an existing post.
    """

    model = Post  # Specifies the model that will be updated
    form_class = (
        PostForm  # Uses a form class for validating post updates
    )
    success_url = "/post-list/"  # Redirects to the post list page upon successful update


# ======================================================================================================================
# PostDeleteView: A class-based view to handle deleting a post
class PostDeleteView(LoginRequiredMixin, DeleteView):
    """
    This view enables authenticated users to delete posts.
    """

    model = Post  # Specifies the model to be deleted
    success_url = "/post-list/"  # Redirects to the post list page upon successful deletion


# ======================================================================================================================
