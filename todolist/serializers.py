from rest_framework import serializers
from todolist.models import Task, TaskActivity, Comment, CommentAttachment, SubTask


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