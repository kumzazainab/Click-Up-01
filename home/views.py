from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework_simplejwt.authentication import JWTAuthentication

from todolist.models import Task
from home.utils import get_greeting_message
from workspace.models import Workspace
from sprint.models import SprintManagement
from user.models import User
from todolist.serializers import TaskSerializer
from workspace.serializers import CreateWorkspaceSerializer
from sprint.serializers import SprintSerializer
from user.serializers import UserSerializer


class SearchViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        search_keyword = request.query_params.get("search", "").strip()

        task_filter = Q(title__icontains=search_keyword) | Q(description__icontains=search_keyword)
        workspace_filter = Q(workspace_name__icontains=search_keyword)
        sprint_filter = Q(title__icontains=search_keyword) | Q(description__icontains=search_keyword)
        user_filter = Q(username__icontains=search_keyword) | Q(profile__full_name__icontains=search_keyword)

        tasks = Task.objects.filter(task_filter)
        workspaces = Workspace.objects.filter(workspace_filter)
        sprints = SprintManagement.objects.filter(sprint_filter)
        users = User.objects.filter(user_filter)

        if not any([tasks.exists(), workspaces.exists(), sprints.exists(), users.exists()]):
            return Response({"error": "No results found."}, status=status.HTTP_404_NOT_FOUND)

        task_data = TaskSerializer(tasks, many=True).data
        workspace_data = CreateWorkspaceSerializer(workspaces, many=True).data
        sprint_data = SprintSerializer(sprints, many=True).data
        user_data = UserSerializer(users, many=True).data

        return Response({
            "search_keyword": search_keyword,
            "total_results": {
                "tasks": len(task_data),
                "workspaces": len(workspace_data),
                "sprints": len(sprint_data),
                "users": len(user_data),
            },
            "tasks": task_data,
            "workspaces": workspace_data,
            "sprints": sprint_data,
            "users": user_data
        }, status=status.HTTP_200_OK)


class GreetingAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user_name = request.user.first_name or request.user.username
        message = get_greeting_message(user_name)
        return Response({"greeting": message})