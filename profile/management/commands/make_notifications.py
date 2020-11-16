from authentication.middleware import get_user_from_passport, update_or_create_user
from django.core.management.base import BaseCommand
from profile.profile_methods.notification_params_validation import polymer_notification_validation
import pickle
polymer_user_relation_file_name = "user_polymers_rel.pkl"
polymers_ids = {
    "535": [5],
    "585": [10, 11],
    "591": [13],
    "ПСМ-Э": [60, 61]

}


class Command(BaseCommand):
    help = "Make polymer notifications for new users"

    def handle(self, *args, **options):
        make_notifications()


def make_notifications():
    data = get_polymer_user_relations()
    for key, value in data.items():
        print(key, "-", value)
        polymer_ids = polymers_ids.get(key)
        if polymer_ids:

            for user_id in value:
                user = get_user_instance(user_id)
                user.cancel_auction_notification = True
                user.creating_auction_notification = True
                user.starting_auction_notification = True
                user.save()

                for polymer_id in polymer_ids:
                    polymer_notification_validation([{"id": polymer_id, "value": True}], user)


def get_polymer_user_relations():
    file = open(polymer_user_relation_file_name, 'rb')
    data = pickle.load(file)
    return data if data else None


def get_user_instance(user_id):
    passport_user = get_user_from_passport(user_id=user_id)
    print(passport_user)
    user = update_or_create_user(passport_user)
    return user
