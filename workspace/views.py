from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from workspace.models import WorkspaceInvitation, Workspace
from workspace.serializers import CreateWorkspaceSerializer, WorkSpaceInvitationSerializer

# Create your views here.

class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = CreateWorkspaceSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class WorkspaceInvitationViewSet(viewsets.ModelViewSet):
    queryset = WorkspaceInvitation.objects.all()
    serializer_class = WorkSpaceInvitationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]