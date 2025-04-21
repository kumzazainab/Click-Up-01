import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from home.models import UUIDModel
from user.models import User
from user.utils import STATUS
from sprint.models import SprintManagement

# Create your models here.

class Task(UUIDModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, related_name='assigned_to', on_delete=models.CASCADE)
    sprints = models.ForeignKey(SprintManagement, related_name='sprints', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='todo')

    def __str__(self):
        return self.title