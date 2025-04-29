from rest_framework import serializers

from sprint.models import SprintManagement, Folder
from todolist.models import Task
from todolist.serializers import TaskSerializer


class SprintSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    class Meta:
        model = SprintManagement
        fields = '__all__'


class SharedFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'