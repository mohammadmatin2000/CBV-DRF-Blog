from django.urls import path
from .views import IndexView, RedirectToMakt, PostDetailView, PostListView, PostFormView

# ======================================================================================================================
# Setting the application namespace to 'blog' for URL reversibility
app_name = 'blog'

# Defining URL patterns for the blog application
urlpatterns = [
    # Maps '/index-class/' to the IndexView class-based view
    path('index-class/', IndexView.as_view(), name='index-class'),

    # Maps '/go-to-makt/' to the RedirectToMakt view, handling redirections
    path("go-to-makt/", RedirectToMakt.as_view(), name='go-to-maktabkhooneh'),

    # Maps '/post-list/' to the PostListView class-based view, displaying all posts
    path('post-list/', PostListView.as_view(), name='post-list'),

    # Maps '/post-list/<int:pk>' to the PostDetailView class-based view, showing a specific post by primary key (pk)
    path('post-list/<int:pk>', PostDetailView.as_view(), name='post-detail'),

    # Maps '/post-create/' to the PostFormView class-based view, handling post creation
    path('post-create/', PostFormView.as_view(), name='post-create'),
]

# ======================================================================================================================