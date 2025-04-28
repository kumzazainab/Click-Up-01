from django.utils import timezone

from django.db import models

from home.models import UUIDModel
from workspace.models import Workspace


# Create your models here.
class SprintManagement(UUIDModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="workspaces", null=True, blank=True)
    folder = models.ForeignKey("sprint.Folder", related_name="sprints", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Folder(UUIDModel):
    name = models.CharField(max_length=255)
    workspace = models.ForeignKey(Workspace, related_name='folders', on_delete=models.CASCADE)

    def __str__(self):
        return self.name