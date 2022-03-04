from datetime import timedelta
import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EcoMail.settings')


BASE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

app = Celery('EcoMail')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule={
    'scrap-data-every-15-minutes':{
        'task':'send_scheduled_mail.tasks.scrap',
        'schedule': timedelta(minutes=15)
    }
}

# app.conf.celery_broker_url = BASE_REDIS_URL
# app.conf.enable_utc = True
app.conf.update(timezone='Asia/Kolkata')
# this allows you to schedule items in the Django admin. CELERY BEAT
app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'




