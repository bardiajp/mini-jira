from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Issue
from .serializers import IssueSerializer


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer

    def get_permission_classes(self):
        if self.action == 'destroy':
            return [IsAdminUser]
        if self.request.user.is_staff:
            return [IsAdminUser, IsAuthenticated]
        return [IsAuthenticated]

    def get_permissions(self):
        return [permission() for permission in self.get_permission_classes()]

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            return Issue.objects.filter(assigned_to=user).order_by('-created_at')
        return Issue.objects.all()

    def perform_create(self, serializer):
        serializer.save(assigned_to=self.request.user)
