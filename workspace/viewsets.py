from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from home.permissions import IsAdminCanDelete
from workspace.models import WorkspaceInvitation, Workspace
from workspace.serializers import CreateWorkspaceSerializer, WorkSpaceInvitationSerializer

# Create your views here.


class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = CreateWorkspaceSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, IsAdminCanDelete]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workspace = serializer.save()
        invitations = request.data.get('invitations', [])
        created_invitations = []
        for email in invitations:
            invitation = WorkspaceInvitation.objects.create(
                workspace=workspace,
                email=email,
                invited_by=request.user
            )
            created_invitations.append({
                "email": invitation.email,
                "invited_on": invitation.invited_on,
                "invited_by": invitation.invited_by.email
            })

        response_data = {
            **serializer.data,
            "invitations": created_invitations
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class WorkspaceInvitationViewSet(viewsets.ModelViewSet):
    queryset = WorkspaceInvitation.objects.all()
    serializer_class = WorkSpaceInvitationSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [JWTAuthentication]