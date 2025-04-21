from django.shortcuts import render

from sprint.models import SprintManagement, Folder
from sprint.serializers import TaskSerializer, SprintSerializer, SharedFolderSerializer
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from todolist.models import Task


# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class SprintViewSet(viewsets.ModelViewSet):
    queryset = SprintManagement.objects.all()
    serializer_class = SprintSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class SharedFolderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = SharedFolderSerializer

    def get_queryset(self):
        workspace_id = self.request.query_params.get('workspace_id')
        if workspace_id:
            return Folder.objects.filter(workspace__id=workspace_id, name__iexact="Shared with Me")
        return Folder.objects.none()