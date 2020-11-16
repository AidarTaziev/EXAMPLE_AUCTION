import requests
import logging
from django.conf import settings

logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'EXAMPLE_AUCTION.log')


def get_polymer_short_info(polymer_id):
    return make_post_request(settings.POLYMER_SPRAV_FULL_URI+"/get_polymer_short_info", {'polymer_id': polymer_id})


def get_all_polymers_short_info():
    return make_post_request(settings.POLYMER_SPRAV_FULL_URI+"/get_all_polymers_short_info")


def get_polymers_ids_for(poly_filters):
    return make_post_request(settings.POLYMER_SPRAV_FULL_URI+"/find_polymers_for", poly_filters)


def get_polymers_type():
    return make_post_request(settings.POLYMER_SPRAV_FULL_URI+"/get_all_plants_types")


def get_all_plants_types():
    return make_post_request(settings.POLYMER_SPRAV_FULL_URI+"/get_all_plants_types")


def get_types_ref_polymers():
    return make_post_request(settings.POLYMER_SPRAV_FULL_URI+"/get_types_ref_polymers")


def make_post_request(full_uri, data=dict()):
    data['api_secret_key'] = settings.POLYMER_SPRAV_SECRET_KEY
    response = requests.post(full_uri, data)
    response.raise_for_status()
    return response.json()


