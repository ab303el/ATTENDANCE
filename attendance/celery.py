import os
from celery import Celery

# Tell Celery to use your Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE' , 'attendance.settings')

app = Celery('attendance')

# Load task modules from all registered Django apps
app.config_from_object('django.conf:settings' , namespace='CELERY')
app.autodiscover_tasks()