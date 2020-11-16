import os
from celery import Celery
from celery.schedules import crontab
from celery.schedules import crontab_parser
from django.conf import settings

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EXAMPLE_AUCTION.settings')

app = Celery('EXAMPLE_AUCTION')
app.config_from_object('django.conf:settings')
app.conf.timezone = settings.TIME_ZONE

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-everyday-in-17': {
        'task': 'EXAMPLE_AUCTION.tasks.send_trade_start_notification',
        'schedule': crontab(minute=0, hour=17)
    },
}
