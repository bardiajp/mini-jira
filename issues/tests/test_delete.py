from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from issues.factories import UserFactory, IssueFactory
from issues.models import Issue


class DeleteIssuesTests(APITestCase):

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
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_delete_other_user_issue(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('issues-detail', kwargs={'pk': self.other_user_issue.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Issue.objects.filter(assigned_to=self.user1).exists())