from rest_framework.test import APIClient
from django.shortcuts import reverse
from accounts.models.users import User
from datetime import datetime
import pytest


# ======================================================================================================================
@pytest.fixture
def client():
    return APIClient()
@pytest.fixture
def user():
    user = User.objects.create_user(email='admin@admin.com', password='m1387m2008m')
    return user
# ======================================================================================================================
@pytest.mark.django_db
class TestPostAPI:
    # def test_get_post_response_200_status(self,client):
    #     url = reverse("blog:api-v1:post-list")
    #     response = client.get(url)
    #     assert response.status_code == 200
    def test_create_post_response_401_status(self, client):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "Test title",
            "content": "Test content",
            "status": 1,

        }
        response = client.post(url, data)
        assert response.status_code == 401
    def test_create_post_response_201_status(self, client, user):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "Test title",
            "content": "Test content",
            "status": 1,
            "published_date": datetime.now(),
            "author": user.id,
        }
        client.force_login(user=user)
        response = client.post(url,data)
        assert response.status_code == 201
# ======================================================================================================================
