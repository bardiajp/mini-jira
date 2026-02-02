from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from issues.factories import UserFactory


class CreateIssueTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user1 = UserFactory(email="user1@test.com")
        self.user2 = UserFactory(email="user2@test.com")
        self.admin_user = UserFactory(email="admin@test.com", is_staff=True)

        # self.issue_user1_1 = IssueFactory(assigned_to=self.user1)
        # self.issue_user1_2 = IssueFactory(assigned_to=self.user1)
        # self.issue_user2_1 = IssueFactory(assigned_to=self.user2)

        self.url = reverse('issues-list')

    # def test_user_can_only_see_own_issues(self):
    #     self.client.force_authenticate(user=self.user1)
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.json()), 2)
    #
    #     returned_ids = [item['id'] for item in response.data]
    #     self.assertIn(self.issue_user1_1.id, returned_ids)
    #     self.assertNotIn(self.issue_user2_1.id, returned_ids)

    def test_not_authenticated(self):
        data = {
            "title": "New Test Issue",
            "description": "Test description",
            "status": 0,
            "priority": 1
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_successful(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            "title": "New Test Issue",
            "description": "Test description",
            "status": 0,
            "priority": 1
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['assigned_to']['email'], self.user1.email)
