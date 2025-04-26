from django.urls import path
from .views import IndexView,RedirectToMakt


# ======================================================================================================================
app_name = 'blog'

urlpatterns = [
    path('indexclass/', IndexView.as_view(), name='indexclass'),
    path("go-to-makt/",RedirectToMakt.as_view(), name='go-to-maktabkhooneh'),
]
