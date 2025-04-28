from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject1.settings')

app = Celery('DjangoProject1')

# Read settings from Django settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks modules from all registered  Django apps
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.conf.beat_schedule = {
    'auto-stop-running-timers-every-5-mins': {
        'task': 'tasks.tasks.stop_running_timers',
        'schedule': crontab(minute='*/5'),  # every 5 minutes
    },
}
