from rest_framework import routers
from .views import PostModelViewSet, CategoryModelViewSet

# ======================================================================================================================
# Setting the application namespace to 'api-v1' for better URL reversibility and organization
app_name = "api-v1"

# Creating a router for automatic URL generation for ViewSets
router = routers.DefaultRouter()

# Registering the PostModelViewSet with the router
# - This automatically generates CRUD API endpoints for the Post model
router.register("post", PostModelViewSet, basename="post")

# Registering the CategoryModelViewSet with the router
# - This provides API routes for managing categories
router.register("category", CategoryModelViewSet, basename="category")

# Using router-generated URLs as the urlpatterns
# - This replaces manually defined paths, making API endpoint management more efficient
urlpatterns = router.urls

# ======================================================================================================================
