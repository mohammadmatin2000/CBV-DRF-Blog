from django.test import TestCase,SimpleTestCase
from ..models import Category
from ..forms import PostForm

# ======================================================================================================================
class TestPostForm(TestCase):
    def test_post_form_valid_data(self):
        form=PostForm(data = {
            'title': 'Test title',
            'content': 'Test content',
            'status': 1,
            'category': Category.objects.create(name='dars')
        })
        self.assertTrue(form.is_valid())
    def test_post_form_no_valid_data(self):
        form=PostForm(data = {})
        self.assertFalse(form.is_valid())
# ======================================================================================================================