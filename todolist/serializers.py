from rest_framework import serializers

from home.utils import parse_time_estimate
from todolist.models import Task, TaskActivity, Comment, CommentAttachment, SubTask, TaskAttachment, TaskStatus, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class TimeEstimateField(serializers.DurationField):

    def to_internal_value(self, value):
        if isinstance(value, str):
            try:
                return parse_time_estimate(value)
            except Exception:
                raise serializers.ValidationError("Time estimate format should be like '1d 2h 30m'")
        return super().to_internal_value(value)


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = ['id', 'name']


class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    status = TaskStatusSerializer()
    time_estimate = TimeEstimateField(required=False, allow_null=True)

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        status = validated_data.pop('status')
        task = Task.objects.create(**validated_data)
        if status:
            status, created = TaskStatus.objects.get_or_create(**status)
            task.status = status
        for tags in tags:
            tag, created = Tag.objects.get_or_create(**tags)
            task.tags.add(tag)

        task.save()
        return task


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