from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from issues.factories import UserFactory, IssueFactory


class RetrieveIssueTests(APITestCase):

    def setUp(self):
        self.user1 = UserFactory(email="user1@test.com")
        self.user2 = UserFactory(email="user2@test.com")
        self.admin_user = UserFactory(email="admin@test.com", is_staff=True)

        self.issue = IssueFactory(assigned_to=self.user1)
        self.other_user_issue = IssueFactory(assigned_to=self.user2)

        self.url = reverse('issues-detail', kwargs={'pk': self.issue.pk})

    def test_not_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["assigned_to"]["email"], self.user1.email)

    def test_user_cannot_delete_other_user_issue(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('issues-detail', kwargs={'pk': self.other_user_issue.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_user(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
