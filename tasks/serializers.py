from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError(
                "Title cannot be empty."
            )

        if len(value.strip()) > 200:
            raise serializers.ValidationError(
                "Title cannot exceed 200 characters."
            )

        return value.strip()

    def validate_description(self, value):
        if value and not value.strip():
            raise serializers.ValidationError(
                "Description cannot contain only spaces."
            )

        return value.strip() if value else value

    def validate_status(self, value):
        allowed_statuses = [
            'Pending',
            'In Progress',
            'Completed'
        ]

        if value not in allowed_statuses:
            raise serializers.ValidationError(
                "Status must be Pending, In Progress, or Completed."
            )

        return value

    def validate_priority(self, value):
        allowed_priorities = [
            'Low',
            'Medium',
            'High'
        ]

        if value not in allowed_priorities:
            raise serializers.ValidationError(
                "Priority must be Low, Medium, or High."
            )

        return value