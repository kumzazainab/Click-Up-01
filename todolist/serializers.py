from rest_framework import serializers
from todolist.models import Task, TaskActivity, Comment, CommentAttachment, SubTask, TaskAttachment

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'

class TaskActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskActivity
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class CommentAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentAttachment
        fields = '__all__'

class TaskAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAttachment
        fields = '__all__'