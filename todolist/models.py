import uuid
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser
from home.models import UUIDModel
from user.models import User
from user.utils import TICKET_PRIORITY
from sprint.models import SprintManagement
from django.utils import timezone

# Create your models here.


class Tag(UUIDModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TaskStatus(UUIDModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Task(UUIDModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, related_name='assigned_to', on_delete=models.CASCADE)
    sprints = models.ForeignKey(SprintManagement, related_name='tasks', on_delete=models.CASCADE, null=True, blank=True)
    status = models.ForeignKey(TaskStatus, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    time_estimate = models.DurationField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    priority = models.CharField(max_length=10, choices=TICKET_PRIORITY, default='normal')
    track_time = models.DurationField(default=timezone.timedelta())
    watchers = models.ManyToManyField(User, related_name='watched_tasks', blank=True)
    due_date = models.DateField(null=True, blank=True)
    all_day = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.status and getattr(self.status, 'name', '').lower() == "complete":
            self.is_completed = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title if self.title else "Untitled Task"


class SubTask(UUIDModel):
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, related_name='subtasks_assigned', on_delete=models.CASCADE)
    status = models.ForeignKey(TaskStatus, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title if self.title else  "Untitled Task"


class TaskActivity(UUIDModel):
    task = models.ForeignKey(Task, related_name='activities', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.action} {self.created_at}"


class TaskAttachment(UUIDModel):
    task = models.ForeignKey(Task, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField()
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class Comment(UUIDModel):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    subject = models.TextField()
    is_email = models.BooleanField(default=False)
    to_users = models.ManyToManyField(User, related_name="email_comment_recipients")
    mentions = models.ManyToManyField(User, related_name='mentioned_in_comments', blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.task}"


class CommentAttachment(UUIDModel):
    task = models.ForeignKey(Task, related_name='comment_attachments', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='comment_attachments/')
    # uploaded_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.file.name
