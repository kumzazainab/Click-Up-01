from django.db.models import Count
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from todolist.models import Task, SubTask, TaskActivity, CommentAttachment, Comment
from todolist.serializers import SubTaskSerializer, TaskActivitySerializer, CommentAttachmentSerializer, \
    CommentSerializer


class AdminTaskReportView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        total_tasks = Task.objects.count()
        completed_tasks = Task.objects.filter(status='done').count()
        tasks_per_user = Task.objects.values('assigned_to__email').annotate(task_count=Count('assigned_to')).order_by('-task_count')
        tasks_by_status = Task.objects.values('status').annotate(status_count=Count('status')).order_by('status')

        report_data = {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "tasks_per_user": tasks_per_user,
            "tasks_by_status": tasks_by_status,
        }

        return Response(report_data, status=status.HTTP_200_OK)

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

class CommentAttachmentViewSet(viewsets.ModelViewSet):
    queryset = CommentAttachment.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CommentAttachmentSerializer