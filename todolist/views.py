from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from sprint.filters import TaskFilter
from todolist.models import Task, SprintManagement, TaskActivity
from todolist.serializers import TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse

from rest_framework import status as drf_status
from home.utils import unfinished_task
from home.permissions import IsAdminOrProjectManager
from todolist.task import stop_timer
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

class StopTimerAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrProjectManager]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        stop_timer.delay()
        return Response({"message": "Timer stop task triggered successfully!"}, status=status.HTTP_200_OK)


class MoveTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def patch(self, request, task_id):
        new_sprint_id = request.data.get("sprint_id")
        user = request.user

        try:
            task = Task.objects.get(id=task_id)
            new_sprint = SprintManagement.objects.get(id=new_sprint_id)
            if task.sprints == new_sprint:
                return Response(
                    {"error": "The task is already in the selected sprint."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            old_sprint = task.sprints
            task.sprints = new_sprint
            task.save()
            action_msg = f"Task with ID '{task.id}' moved from sprint '{old_sprint.title if old_sprint else 'None'}' to sprint '{new_sprint.title}'"
            TaskActivity.objects.create(
                task=task,
                user=user,
                action=action_msg
            )
            return Response({
                "action_message": action_msg,
                "task_id": task.id,
                "user_id": user.id
            }, status=status.HTTP_200_OK)

        except Task.DoesNotExist:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
        except SprintManagement.DoesNotExist:
            return Response({"error": "Sprint not found."}, status=status.HTTP_404_NOT_FOUND)


class UnfinishedTasksView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, sprint_id):
        unfinished_tasks = Task.objects.filter(sprints__id=sprint_id, is_completed=False)
        serializer = TaskSerializer(unfinished_tasks, many=True)
        response_data = {
            'unfinished_tasks': serializer.data,
            'message': f"This sprint has {unfinished_tasks.count()} unfinished tasks."
        }
        return Response(response_data, status=status.HTTP_200_OK)


class TaskListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, sprint_id):
        tasks = Task.objects.all().order_by('status')
        # Filter handling
        task_filter = TaskFilter(request.GET, queryset=tasks, request=request)
        tasks = task_filter.qs
        grouped_tasks = {}
        for task in tasks:
            status_key = str(task.status)
            if status_key not in grouped_tasks:
                grouped_tasks[status_key] = []
            grouped_tasks[status_key].append(task)

        serialized_grouped_tasks = {status_key: TaskSerializer(group, many=True).data for status_key, group in grouped_tasks.items()}
        unfinished_tasks = unfinished_task(sprint_id, request)

        response_data = {
            'grouped_tasks': serialized_grouped_tasks,
            'unfinished_tasks': unfinished_tasks
        }
        return Response(response_data, status=status.HTTP_200_OK)


class TaskTableView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, sprint_id):
        tasks = Task.objects.filter(sprint_id=sprint_id).order_by('status')
        # Filter handling
        task_filter = TaskFilter(request.GET, queryset=tasks, request=request)
        tasks = task_filter.qs
        serializer = TaskSerializer(tasks, many=True)
        unfinished_tasks = unfinished_task(sprint_id, request)
        response_data = {
            'tasks': serializer.data,
            'unfinished_tasks': unfinished_tasks
        }
        return Response(response_data, status=status.HTTP_200_OK)


class TaskBoardView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, sprint_id):
        tasks = Task.objects.select_related('status', 'assigned_to').prefetch_related('tags', 'watchers', 'sprints').all()
        # Filter handling
        task_filter = TaskFilter(request.GET, queryset=tasks, request=request)
        tasks = task_filter.qs
        grouped_tasks = {}
        for task in tasks:
            status_name = task.status.name if task.status else "No Status"
            grouped_tasks.setdefault(status_name, []).append(task)

        result = [
            {
                "status": status_name,
                "tasks": TaskSerializer(tasks, many=True).data
            }
            for status_name, tasks in grouped_tasks.items()
        ]
        unfinished_tasks = unfinished_task(sprint_id, request)
        response_data = {
            'grouped_tasks': result,
            'unfinished_tasks': unfinished_tasks
        }
        return Response(response_data, status=drf_status.HTTP_200_OK)


@csrf_exempt
def send_email(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON."}, status=400)

    subject = data.get('subject')
    message = data.get('message')
    from_email = data.get('from_email')
    recipient_list = data.get('recipient_list', [])

    if not all([subject, message, from_email, recipient_list]):
        return JsonResponse({"error": "Missing required fields."}, status=400)

    send_mail(subject, message, from_email, recipient_list)
    return JsonResponse({"message": "Email sent successfully!"}, status=200)