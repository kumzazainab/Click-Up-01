from datetime import timedelta

from django.utils import timezone
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from home.permissions import IsAdminOrProjectManager
from todolist.models import Task, SubTask, TaskActivity, CommentAttachment, Comment, TaskAttachment, Tag, TaskStatus
from todolist.serializers import SubTaskSerializer, TaskActivitySerializer, CommentAttachmentSerializer, \
    CommentSerializer, TaskAttachmentSerializer, TaskSerializer, TagSerializer, TaskStatusSerializer, TaskCalendarSerializer
from home.utils import extract_tagged_users


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        task_param = self.request.query_params.get('task', None)

        if task_param == 'home':
            seven_days_ago = timezone.now() - timedelta(days=7)
            return Task.objects.filter(created_at__gte=seven_days_ago)
        else:
            return Task.objects.all()

    def get_queryset(self):
        user = self.request.user
        task_param = self.request.query_params.get('task', None)

        if task_param == 'assigned_to_me':
            return Task.objects.filter(assigned_to=user)
        else:
            return Task.objects.all()


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, IsAdminOrProjectManager]
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


class CalendarViewSet(viewsets.ModelViewSet):
    serializer_class = TaskCalendarSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        queryset = Task.objects.filter(assigned_to=user)
        if start and end:
            queryset = queryset.filter(start_date__gte=start, end_date__lte=end)
        return queryset
