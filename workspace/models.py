import uuid

from django.db import models

from home.models import UUIDModel
from user.models import User
from user.utils import WORKSPACE_TYPES, MANAGE_TYPES, TOOLS_CHOICES, RESOURCE_CHOICES, FEATURES_CHOICES
from django.contrib.postgres.fields import ArrayField


class Workspace(UUIDModel):
    workspace_name = models.CharField(unique=True, max_length=255)
    workspace_type = models.CharField(choices=WORKSPACE_TYPES)
    manage_type = models.CharField(choices=MANAGE_TYPES)
    resource = models.CharField(choices=RESOURCE_CHOICES, max_length=255)
    tools = ArrayField(models.CharField(choices=TOOLS_CHOICES))
    features = ArrayField(models.CharField(choices=FEATURES_CHOICES, max_length=255))

    def __str__(self):
        return self.workspace_name


class WorkspaceInvitation(UUIDModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    email = models.EmailField()
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    invited_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email