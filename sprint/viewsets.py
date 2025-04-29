from sprint.models import SprintManagement, Folder
from sprint.serializers import SprintSerializer, SharedFolderSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from todolist.models import Task
from home.permissions import IsAdminOrProjectManager
# Create your views here.


class SprintViewSet(viewsets.ModelViewSet):
    queryset = SprintManagement.objects.all()
    serializer_class = SprintSerializer
    permission_classes = [IsAuthenticated, IsAdminOrProjectManager]
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