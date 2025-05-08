from django.urls import path, include
from .views import (
    IndexView,
    RedirectToMakt,
    PostDetailView,
    PostListView,
    PostFormView,
    PostUpdateView,
    PostDeleteView,
)

# ======================================================================================================================
# Setting the application namespace to 'blog' for URL reversibility, making URL names unique in different apps
app_name = "blog"

# Defining URL patterns for the blog application
urlpatterns = [
    # Maps '/index-class/' to the IndexView class-based view
    path("index-class/", IndexView.as_view(), name="index-class"),
    # Maps '/go-to-makt/' to the RedirectToMakt view, handling redirections to an external URL
    path(
        "go-to-makt/",
        RedirectToMakt.as_view(),
        name="go-to-maktabkhooneh",
    ),
    # Maps '/post-list/' to the PostListView class-based view, displaying all blog posts
    path("post-list/", PostListView.as_view(), name="post-list"),
    # Maps '/post-list/<int:pk>' to the PostDetailView class-based view, showing a specific post by primary key (pk)
    path(
        "post-list/<int:pk>",
        PostDetailView.as_view(),
        name="post-detail",
    ),
    # Maps '/post-create/' to the PostFormView class-based view, handling post creation through a form
    path("post-create/", PostFormView.as_view(), name="post-create"),
    # Maps '/post-update/<int:pk>' to the PostUpdateView class-based view, allowing post updates by primary key
    path(
        "post-update/<int:pk>",
        PostUpdateView.as_view(),
        name="post-update",
    ),
    # Maps '/post-delete/<int:pk>' to the PostDeleteView class-based view, enabling post deletion by primary key
    path(
        "post-delete/<int:pk>",
        PostDeleteView.as_view(),
        name="post-delete",
    ),
    path("api/v1/", include("blog.api.v1.urls")),
]

# ======================================================================================================================
