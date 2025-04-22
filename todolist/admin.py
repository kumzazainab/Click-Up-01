from django.contrib import admin
from todolist.models import Task, TaskActivity, SubTask, Comment, CommentAttachment

# Register your models here.

admin.site.register(Task)
admin.site.register(SubTask)
admin.site.register(TaskActivity)
admin.site.register(Comment)
admin.site.register(CommentAttachment)