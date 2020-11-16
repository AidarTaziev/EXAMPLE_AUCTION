import logging
import requests
from django.conf import settings


def get_user_info(user_id):
    return make_post_request(settings.PASSPORT_USER_CREDENTIALS_URI, {'user_id': user_id})


def make_post_request(full_uri, data=dict()):
    try:
        data['secret'] = settings.PASSPORT_SECRET_KEY
        response = requests.post(full_uri, data)
        response.raise_for_status()
        return response.json()
    except Exception as ex:
        logging.error(ex)
