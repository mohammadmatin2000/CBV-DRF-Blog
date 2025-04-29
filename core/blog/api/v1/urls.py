from django.urls import path
from .views import post_listview, post_detailview

# ======================================================================================================================
# Setting the application namespace to 'api-v1' for better URL reversibility and organization
app_name = 'api-v1'

# Defining URL patterns for the API endpoints
urlpatterns = [
    # Maps '/post/' to the post_listview function, returning a list of all published posts
    path('post/', post_listview, name='post_list'),

    # Maps '/post/<int:id>/' to the post_detailview function, retrieving a specific post by its ID
    path('post/<int:id>/', post_detailview, name='post_detail'),
]
# ======================================================================================================================