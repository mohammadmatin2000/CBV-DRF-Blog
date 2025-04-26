from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView,RedirectView
from .models import Post
# ======================================================================================================================

class IndexView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Blog'
        context['posts'] = Post.objects.all()
        return context
# ======================================================================================================================
class RedirectToMakt(RedirectView):
    url = 'https://maktabkhooneh.com/'
# ======================================================================================================================