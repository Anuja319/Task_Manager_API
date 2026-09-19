from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import Task
from .serializers import TaskSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def task_list(request):

    # GET - Get all tasks
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # POST - Create a new task
    if request.method == 'POST':
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
def register(request):

    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {
                "error": "Username and password are required."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if len(password) < 8:
        return Response(
            {
                "error": "Password must be at least 8 characters long."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {
                "error": "Username already exists."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        username=username,
        password=password
    )

    token, created = Token.objects.get_or_create(user=user)

    return Response(
        {
            "message": "User registered successfully",
            "token": token.key
        },
        status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
def login(request):

    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {
                "error": "Username and password are required."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(
        username=username,
        password=password
    )

    if user is None:
        return Response(
            {
                "error": "Invalid username or password."
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    token, created = Token.objects.get_or_create(user=user)

    return Response(
        {
            "message": "Login successful",
            "token": token.key
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_detail(request, pk):

    # Find the task
    try:
        task = Task.objects.get(pk=pk)

    except Task.DoesNotExist:
        return Response(
            {"error": "Task not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    # GET - Get one task
    if request.method == 'GET':
        serializer = TaskSerializer(task)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # PUT - Update task
    if request.method == 'PUT':
        serializer = TaskSerializer(
            task,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE - Delete task
    if request.method == 'DELETE':
        task.delete()

        return Response(
            {"message": "Task deleted successfully."},
            status=status.HTTP_200_OK
        )