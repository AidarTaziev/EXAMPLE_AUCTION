import logging
from datetime import datetime, timedelta
from django.db.models import Q
from auction.models import Auction, AuctionParticipationOrder
from sprav.requests import get_polymers_ids_for
from utils.time_customization.custom_time import current_datetime


logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG, filename=u'EXAMPLE_AUCTION.log')


def get_current_auctions_bids_qs(status):
    if status == 'all':
        return get_all_auction_bids_qs()
    elif status == 'active':
        return get_active_auction_bids_qs()
    elif status == 'archive':
        return get_finished_auction_bids_qs()
    else:
        return get_planning_auction_bids_qs()


def get_all_auction_bids_qs():
    now = datetime.now()
    start = datetime(now.year, now.month, now.day)
    bids = Auction.objects.filter(start_bidding__gte=start).order_by('start_bidding', '-published_datetime')
    return bids


def get_active_auction_bids_qs():
    """
        Выводит все активные заявки аукциона
        :return polymers - словарь со свойствами заявки аукциона:
    """

    now = datetime.now()
    bids = Auction.objects.filter(start_bidding__lte=now, end_bidding__gt=now).exclude(is_finished=True).\
        order_by('start_bidding', '-published_datetime')

    return bids


# def get_finished_auction_bids():
#     """
#         Выводит все прошедшие заявки аукциона
#         :return polymers - словарь со свойствами заявки аукциона:
#     """
#
#     now = current_datetime()
#     bids = EXAMPLE_AUCTION.objects.filter(end_bidding__lte=now).order_by('-start_bidding', '-published_datetime')
#     return bids


def get_finished_auction_bids_qs():
    """
        Выводит все прошедшие заявки аукциона
        :return polymers - словарь со свойствами заявки аукциона:
    """

    now = current_datetime()
    bids = Auction.objects.filter(Q(end_bidding__lte=now) | Q(is_finished=True)).order_by('-start_bidding', '-published_datetime')
    return bids


def get_today_finished_auction_bids_qs():
    """
        Выводит все прошедшие заявки аукциона
        :return polymers - словарь со свойствами заявки аукциона:
    """

    now = datetime.now()
    start = datetime(now.year, now.month, now.day)
    end = start + timedelta(days=1)

    bids = Auction.objects.filter(end_bidding__gte=start, end_bidding__lt=end, is_finished=True)\
        .order_by('-start_bidding', '-published_datetime')

    return bids


def get_planning_auction_bids_qs():
    """
        Выводит все планируемые заявки аукциона
        :return polymers - словарь со свойствами заявки аукциона:
    """
    now = current_datetime()
    bids = Auction.objects.filter(start_bidding__gt=now).order_by('start_bidding', '-published_datetime')
    return bids


def get_polymer_shortcode_qs(qs, polymer_shortcode):
    qs = qs.filter(polymer__shortcode__contains=polymer_shortcode)
    return qs


def get_polymer_type_qs(qs, polymer_type):
    qs = qs.filter(polymer__subtype__type=polymer_type)
    return qs


def get_polymer_for_types_qs(qs, polymer_plant_name):
    qs = qs.filter(polymer__subtype__type__name__icontains=polymer_plant_name)
    return qs


def get_polymer_plant_qs(qs, polymer_plant):
    qs = qs.filter(polymer__plants=polymer_plant)
    return qs


def get_company_allowed_auctions_ids(company):
    allowed_order = AuctionParticipationOrder.objects.filter(company=company, participation_status=1)
    allowed_auctions_ids = [order.auction.id for order in allowed_order]
    return allowed_auctions_ids


def get_my_auctions_qs(auction_qs, user):
    return auction_qs.filter(seller=user)


def polymer_filter_qs(qs, polymer_shortcode, polymer_type, polymer_plant):
    poly_filters = {'shortcode': polymer_shortcode,
                    'type': polymer_type,
                    'plant': polymer_plant
                    }
    polymers_ids = get_polymers_ids_for(poly_filters)
    qs = qs.filter(polymer_id__in=polymers_ids)
    return qs