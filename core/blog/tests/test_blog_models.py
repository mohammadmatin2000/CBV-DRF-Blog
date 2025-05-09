from django.test import TestCase
from datetime import datetime
from ..models import Post
from accounts.models.profiles import Profile,User

# ======================================================================================================================
class TestPostModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.com', password='m1387m2008m')
        self.profile = Profile.objects.create(
            user=self.user,
            first_name='test_first_name',
            last_name='test_last_name',
        )
    def test_create_post_model(self):

        post = Post.objects.create(
            title='Test title',
            author=self.profile,  # Ensure this is correct
            content='Test content',
            status=1,
            category=None,
            published_date=datetime.now(),
        )

        self.assertTrue(Post.objects.filter(id=post.id).exists())
        self.assertEqual(post.title, 'Test title')
# ======================================================================================================================
