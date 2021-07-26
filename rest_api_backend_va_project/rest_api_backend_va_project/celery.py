import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest_api_backend_va_project.settings')

app = Celery('celery_task')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
