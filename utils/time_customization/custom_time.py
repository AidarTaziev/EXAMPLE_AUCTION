import pytz
from datetime import datetime, timedelta


utc = pytz.UTC # параметр для локализация времени


def current_datetime():

    return datetime.now()


def replace_to_utc(date_time):

    return date_time.replace(tzinfo=utc)
