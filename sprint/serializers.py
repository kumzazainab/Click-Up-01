from rest_framework import serializers

from sprint.models import SprintManagement, Folder
from todolist.models import Task


class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = SprintManagement
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class SharedFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'