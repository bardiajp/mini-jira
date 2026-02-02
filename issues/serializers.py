from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Issue
from accounts.serializers import UserSerializer

class IssueSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'status', 'priority', 'assigned_to', 'created_at']
        read_only_fields = ['id', 'created_at', "assigned_to"]

    def create(self, validated_data):
        validated_data['assigned_to'] = self.context['request'].user
        return super().create(validated_data)
