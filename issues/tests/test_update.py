from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from issues.factories import UserFactory, IssueFactory


class UpdateIssueTests(APITestCase):

    def setUp(self):
        self.user1 = UserFactory(email="user1@test.com")
        self.user2 = UserFactory(email="user2@test.com")
        self.admin_user = UserFactory(email="admin@test.com", is_staff=True)

        self.issue = IssueFactory(assigned_to=self.user1)
        self.other_user_issue = IssueFactory(assigned_to=self.user2)

        self.url = reverse('issues-detail', kwargs={'pk': self.issue.pk})

    def test_not_authenticated(self):
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            "title": "updated title",
        }
        response = self.client.patch(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.issue.refresh_from_db()
        self.assertEqual(response.json()["title"], data["title"])

    def test_user_cannot_delete_other_user_issue(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            "title": "updated title",
        }
        response = self.client.patch(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "title": "updated title",
        }
        response = self.client.patch(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.issue.refresh_from_db()
        self.assertEqual(response.json()["title"], data["title"])

    def test_update_read_only_fields(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            "id": 1234,
        }
        response = self.client.patch(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.issue.refresh_from_db()
        self.assertNotEqual(self.issue.pk, 1234)

    def test_update_assignee(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            "assigned_to": self.user2.pk,
        }
        response = self.client.patch(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.issue.refresh_from_db()
        self.assertNotEqual(self.issue.pk, self.user2.pk)

