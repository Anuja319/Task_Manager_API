import pytest
from tasks.models import Task
from tasks.serializers import TaskSerializer


@pytest.mark.django_db
def test_task_creation():
    task = Task.objects.create(
        title="Complete assignment",
        description="Finish WA-5",
        status="Pending",
        priority="High"
    )

    assert task.title == "Complete assignment"
    assert str(task) == "Complete assignment"


def test_valid_task_serializer():
    data = {
        "title": "Learn Django",
        "description": "Practice REST API",
        "status": "Pending",
        "priority": "High"
    }

    serializer = TaskSerializer(data=data)

    assert serializer.is_valid()


def test_empty_title_validation():
    data = {"title": "   "}

    serializer = TaskSerializer(data=data)

    assert not serializer.is_valid()
    assert "title" in serializer.errors


def test_invalid_status_validation():
    data = {
        "title": "Learn Python",
        "status": "Started"
    }

    serializer = TaskSerializer(data=data)

    assert not serializer.is_valid()
    assert "status" in serializer.errors


def test_invalid_priority_validation():
    data = {
        "title": "Learn React",
        "priority": "Urgent"
    }

    serializer = TaskSerializer(data=data)

    assert not serializer.is_valid()
    assert "priority" in serializer.errors