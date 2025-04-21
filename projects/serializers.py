from rest_framework import serializers
from projects.models import Project
from user.models import User

class ProjectSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)
    class Meta:
        model = Project
        fields = '__all__'