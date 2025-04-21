from django.db.models import Count
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from todolist.models import Task

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
