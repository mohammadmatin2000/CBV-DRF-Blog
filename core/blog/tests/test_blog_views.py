from django.test import TestCase,Client
from django.urls import reverse
from accounts.models.profiles import Profile,User
from ..models import Post
from datetime import datetime
# ======================================================================================================================
class TestBlogViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email='test@test.com', password='m1387m2008m')
        self.profile = Profile.objects.create(
            user=self.user,
            first_name='test_first_name',
            last_name='test_last_name',
        )
        self.post = Post.objects.create(
            title='Test title',
            author=self.profile,  # Ensure this is correct
            content='Test content',
            status=1,
            category=None,
            published_date=datetime.now(),
        )

    def test_blog_post_successful_response(self):
        url = reverse('blog:index-class')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(response.content))
        self.assertTemplateUsed(response, 'index.html')
    def test_blog_post_detail_login_response(self):
        url = reverse('blog:post-detail', kwargs={'pk': self.post.id})
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    def test_blog_post_detail_anonymous_response(self):
        url=reverse('blog:post-detail', kwargs={'pk':self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
# ======================================================================================================================