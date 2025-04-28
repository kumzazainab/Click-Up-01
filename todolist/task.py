from celery import shared_task
from todolist.models import Task
from django.utils import timezone


@shared_task
def stop_timer():
    now = timezone.now()
    running_tasks = Task.objects.filter(end_date__lt=now)

    for task in running_tasks:
        if task.track_time:
            task.track_time = task.time_estimate
            task.save()
            print(f"Timer auto-stopped for task: {task.title}")

    return f"Stopped {running_tasks.count()} timers."
