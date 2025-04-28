from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from todolist.models import Task, SubTask, TaskActivity, CommentAttachment, Comment, TaskAttachment, Tag, TaskStatus
from todolist.serializers import SubTaskSerializer, TaskActivitySerializer, CommentAttachmentSerializer, \
    CommentSerializer, TaskAttachmentSerializer, TaskSerializer, TagSerializer, TaskStatusSerializer
from todolist.utils import extract_tagged_users


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class TaskStatusViewSet(viewsets.ModelViewSet):
    queryset = TaskStatus.objects.all()
    serializer_class = TaskStatusSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = SubTaskSerializer


class TaskActivityViewSet(viewsets.ModelViewSet):
    queryset = TaskActivity.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = TaskActivitySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        comment = serializer.save(user=self.request.user)
        tagged_users = extract_tagged_users(comment.subject)
        comment.mentions.set(tagged_users)

    def perform_update(self, serializer):
        comment = serializer.save()
        tagged_users = extract_tagged_users(comment.subject)
        comment.mentions.set(tagged_users)


class CommentAttachmentViewSet(viewsets.ModelViewSet):
    queryset = CommentAttachment.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CommentAttachmentSerializer


class TaskAttachmentViewSet(viewsets.ModelViewSet):
    queryset = TaskAttachment.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = TaskAttachmentSerializer