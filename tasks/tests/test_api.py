import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from tasks.models import Task


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        password="testpassword123"
    )


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.mark.django_db
def test_user_registration(api_client):
    response = api_client.post("/api/register/", {
        "username": "newuser",
        "password": "password123"
    })

    assert response.status_code == 201
    assert "token" in response.data


@pytest.mark.django_db
def test_registration_with_short_password(api_client):
    response = api_client.post("/api/register/", {
        "username": "newuser",
        "password": "123"
    })

    assert response.status_code == 400


@pytest.mark.django_db
def test_user_login(api_client, user):
    response = api_client.post("/api/login/", {
        "username": "testuser",
        "password": "testpassword123"
    })

    assert response.status_code == 200
    assert "token" in response.data


@pytest.mark.django_db
def test_login_with_wrong_password(api_client, user):
    response = api_client.post("/api/login/", {
        "username": "testuser",
        "password": "wrongpassword"
    })

    assert response.status_code == 401


@pytest.mark.django_db
def test_unauthorized_task_access(api_client):
    response = api_client.get("/api/tasks/")

    assert response.status_code == 401


@pytest.mark.django_db
def test_create_task(authenticated_client):
    response = authenticated_client.post("/api/tasks/", {
        "title": "Complete WA-5",
        "description": "Write API tests",
        "status": "Pending",
        "priority": "High"
    })

    assert response.status_code == 201
    assert response.data["title"] == "Complete WA-5"


@pytest.mark.django_db
def test_create_task_with_invalid_data(authenticated_client):
    response = authenticated_client.post("/api/tasks/", {
        "title": "   "
    })

    assert response.status_code == 400


@pytest.mark.django_db
def test_get_tasks(authenticated_client):
    Task.objects.create(title="Task One")

    response = authenticated_client.get("/api/tasks/")

    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_get_single_task(authenticated_client):
    task = Task.objects.create(title="Test Task")

    response = authenticated_client.get(
        f"/api/tasks/{task.id}/"
    )

    assert response.status_code == 200
    assert response.data["title"] == "Test Task"


@pytest.mark.django_db
def test_update_task(authenticated_client):
    task = Task.objects.create(title="Old Title")

    response = authenticated_client.put(
        f"/api/tasks/{task.id}/",
        {
            "title": "Updated Title",
            "description": "Updated description",
            "status": "Completed",
            "priority": "High"
        }
    )

    assert response.status_code == 200
    assert response.data["title"] == "Updated Title"


@pytest.mark.django_db
def test_delete_task(authenticated_client):
    task = Task.objects.create(title="Delete Me")

    response = authenticated_client.delete(
        f"/api/tasks/{task.id}/"
    )

    assert response.status_code == 200
    assert not Task.objects.filter(id=task.id).exists()


@pytest.mark.django_db
def test_task_not_found(authenticated_client):
    response = authenticated_client.get("/api/tasks/9999/")

    assert response.status_code == 404