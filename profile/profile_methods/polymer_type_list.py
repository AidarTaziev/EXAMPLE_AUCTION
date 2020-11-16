from sprav.requests import get_types_ref_polymers
from profile import models as profile_models


def get_polymer_ids():
    from sprav.requests import get_all_polymers_short_info

    polymers = get_all_polymers_short_info()

    result = list()

    for type in polymers:
        result.append(type['id'])

    return result


def get_user_polymers_list(user):
    user_types = profile_models.PolymerNotifications.objects.filter(client=user)

    print('get user polymers list', user_types)
    types_ref_polymers = get_types_ref_polymers()

    result = []

    for type in types_ref_polymers:
        polys_count = 0

        if user_types:
            for polymer in type['polymers']:
                if user_types.filter(polymer_id=polymer['id']).exists():
                    polymer['followed'] = True
                    polys_count += 1

        if len(type['polymers']) == polys_count: notification_value = True
        else: notification_value = False

        result.append({
            'id': type['type']['id'],
            'name': type['type']['name'],
            'followed': notification_value,
            'polymers': type['polymers']
        })

    return result
