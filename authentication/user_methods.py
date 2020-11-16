import logging
from django.contrib.sessions.models import Session
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from profile import models as profile_models
from auction.models import Auction

logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'EXAMPLE_AUCTION.log')

User = get_user_model()

def get_user_for_cookie(session_key):
    session = Session.objects.get(session_key=session_key)
    uid = session.get_decoded().get('_auth_user_id')
    user = User.objects.get(pk=uid)

    return user


def get_users_from_group(group_name):

    return Group.objects.get(name=group_name).user_set.all()


# def get_users_emails_for_trade_offer(EXAMPLE_AUCTION):
#     """
#     Возращает список пользовательских емейлов, в соответствии с уровнем аукциона.
#     :param auctionBidId: id аукциона
#     :return: list словарей пользователльских емейлов
#     """
#
#     queryset = User.objects
#     if EXAMPLE_AUCTION.is_dev_bid:
#         users_in_group = get_users_from_group("dev-tester")
#         queryset = queryset.filter(id__in=users_in_group)
#     else:
#         queryset = queryset.filter(creating_auction_notification=True)
#
#     users_emails = []
#
#     for user in queryset:
#         if have_polymer_type_in_notifications(user, EXAMPLE_AUCTION.polymer.subtype.type.id):
#             users_emails.append(user.email)
#
#     return users_emails


def get_users_followed_for(filter_params, polymer_id):
    """
    Возращает список пользовательских емейлов, соответсвующих параметрам фильтрации и подписанных на данный вид полимера
    :param polymer_id: id - типа полимера
    :return: list пользователльских емейлов
    """
    from authentication.middleware import sync_user

    user_emails = []
    users_qs = User.objects.filter(**filter_params)
    for user in users_qs:
        try:
            user = sync_user(user.id)
            if user:
                if user.is_active:
                    if have_polymer_in_notifications(user, polymer_id):
                        user_emails.append(user.email)
                    elif not have_any_polymer_notification(user):
                        user_emails.append(user.email)
        except Exception as ex:
            logging.warning('User {user} exception: {ex}'.format(user=user, ex=ex))

    return user_emails


def user_followed_on_auctions(user, auction_notifications_list):
    user_auction_ids = []
    for id in auction_notifications_list:
        auction = Auction.objects.get(id=id)
        if have_polymer_in_notifications(user, auction.polymer_id):
            user_auction_ids.append(id)

    return user_auction_ids


def have_polymer_in_notifications(user, polymer):
    user_notification_types = profile_models.PolymerNotifications.objects.filter(polymer_id=polymer, client=user)
    return user_notification_types.exists()


def have_any_polymer_notification(user):
    user_notification_types = profile_models.PolymerNotifications.objects.filter(client=user)
    return user_notification_types.exists()


def get_user_for(user_id):
    return User.objects.get(id=user_id)


def get_company_users(company):
    company_users = User.objects.filter(company=company)
    return company_users


def get_dev_emails():
    return Group.objects.get(name='dev-tester').user_set.all().values('email')


