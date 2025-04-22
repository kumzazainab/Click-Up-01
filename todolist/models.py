import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from home.models import UUIDModel
from user.models import User
from user.utils import STATUS
from sprint.models import SprintManagement
from django.utils import timezone

# Create your models here.

class Task(UUIDModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, related_name='assigned_to', on_delete=models.CASCADE)
    sprints = models.ForeignKey(SprintManagement, related_name='sprints', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='todo')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class SubTask(UUIDModel):
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, related_name='subtasks_assigned', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class TaskActivity(models.Model):
    task = models.ForeignKey(Task, related_name='activities', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.action} {self.created_at}"

class Comment(UUIDModel):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.TextField()
    is_email = models.BooleanField(default=False)
    mentions = models.ManyToManyField(User, related_name='mentioned_in_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.task}"

class CommentAttachment(models.Model):
    comment = models.ForeignKey(Comment, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='comment_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
