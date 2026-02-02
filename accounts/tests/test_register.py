from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from accounts.models import User


class RegisterUserTests(APITestCase):

    def setUp(self):
        self.url = reverse("user-register")
        self.payload = {
            'email': 'test@example.com',
            'full_name': 'Test User',
            'password': 'StrongPass123'
        }

    def test_successful(self):
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.email, self.payload['email'])
        self.assertTrue(user.check_password(self.payload['password']))

    def test_register_duplicate_email_fails(self):
        User.objects.create_user(**self.payload)
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
