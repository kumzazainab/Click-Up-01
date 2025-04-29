import re
from django.contrib.auth import get_user_model
from datetime import timedelta
from datetime import datetime
from todolist.models import Task
from rest_framework.reverse import reverse
from django.utils import timezone

User = get_user_model()


def extract_tagged_users(comment_text):
    tagged_usernames = re.findall(r"@(\w+)", comment_text)
    if not tagged_usernames:
        return User.objects.none()
    return User.objects.filter(username__in=tagged_usernames)


def parse_time_estimate(time_str):
    total_minutes = 0
    matches = re.findall(r'(\d+)\s*(d|h|m)', time_str.lower())
    for value, unit in matches:
        value = int(value)
        if unit == 'd':
            total_minutes += value * 1440
        elif unit == 'h':
            total_minutes += value * 60
        elif unit == 'm':
            total_minutes += value
    return timedelta(minutes=total_minutes)


def get_greeting_message(user_name):
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        greeting = "Good Morning"
    elif 12 <= current_hour < 17:
        greeting = "Good Afternoon"
    elif 17 <= current_hour < 21:
        greeting = "Good Evening"
    else:
        greeting = "Good Night"

    return f"{greeting}, {user_name.capitalize()}"


def unfinished_task(sprint_id, request):
    unfinished_tasks = Task.objects.filter(sprints__id=sprint_id, is_completed=False)
    count = unfinished_tasks.count()
    message = (
        f"This sprint has {count} unfinished tasks"
        if count > 0 else
        "This sprint has no unfinished tasks"
    )
    url = reverse('unfinished_tasks', args=[sprint_id], request=request)

    return {
        'unfinished_tasks_message': message,
        'unfinished_tasks_link': url
    }