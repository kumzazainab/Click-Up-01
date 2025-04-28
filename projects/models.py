from django.db import models
from home.models import UUIDModel
from user.utils import STATUS_CHOICES
import uuid
from user.models import User


# Create your models here.
class Project(UUIDModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    members = models.ManyToManyField(User, related_name='projects', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
