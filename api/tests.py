from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Profile, User


class ViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.client = APIClient()
        resp = self.client.post(
            "/authen/jwt/create/",
            {"email": "testuser@example.com", "password": "testpassword"},
            format="json",
        )

        self.token = resp.data["access"]

    def test_create_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + self.token)

        url = reverse("user:profile-list")
        data = {
            "nickName": "nickname",
            "img": "http://127.0.0.1:8000/media/avatars/example.com/img.jpg",
        }
        response = self.client.post(url, data)
        import pdb

        pdb.set_trace()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.get().nickName, "nickname")
        self.assertEqual(Profile.objects.get().userProfile, self.user)
        self.assertEqual(Profile.objects.get().img, "http://example.com/img.jpg")

        self.client.logout()
