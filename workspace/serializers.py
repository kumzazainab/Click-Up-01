from rest_framework import serializers

from workspace.models import Workspace, WorkspaceInvitation


class CreateWorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = '__all__'

class WorkSpaceInvitationSerializer(serializers.ModelSerializer):
    invitations = serializers.ListField(child=serializers.EmailField(), required=False, allow_empty=True)
    class Meta:
        model = WorkspaceInvitation
        fields = '__all__'