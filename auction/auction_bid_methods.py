import logging
import threading
from django.db.models import Max
from django.contrib.auth import get_user_model
from auction.models import Auction, AuctionSellerOffer
from authentication.user_methods import get_users_from_group
from utils.time_customization.custom_time import current_datetime, replace_to_utc
from .auction_bids_list_methods import get_polymer_plant_qs, get_polymer_shortcode_qs, get_polymer_type_qs, \
    get_polymer_for_types_qs


logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'EXAMPLE_AUCTION.log')


def get_auction_bid(auction_id):
    '''
    Функция, возвращающая объект аукциона по id
    :param auction_id: int - id аукциона
    :return: объект - аукциона
    '''

    bid = Auction.objects.get(id=auction_id)
    return bid


def get_auction_seller_offer(seller_offer_id):
    '''
    Функция, возвращающая объект аукциона по id
    :param seller_offer_id: int - id торгового предложения продавца
    :return: объект - торговое предложение продавца
    '''

    offer = AuctionSellerOffer.objects.get(id=seller_offer_id)
    return offer


def save_seller_offer(added_seller_offer):
    '''
    Функция, сохраняющая добавленную ставку.
    :param added_seller_offer: dict - добавленная ставка
    :return: объект - добавленная ставка
    '''

    from auction.forms import AuctionSellersOffersForm

    auction_id = added_seller_offer['EXAMPLE_AUCTION']
    auction = get_auction_bid(auction_id)

    auctionsellerOfferForm = AuctionSellersOffersForm(added_seller_offer)
    if auctionsellerOfferForm.is_valid():
        if auction.current_seller_offer:
            if auction.num_free_lots:
                auction.current_seller_offer.close()
            else:
                auction.current_seller_offer.delete()
        added_seller_offer = auctionsellerOfferForm.save()
        added_seller_offer = get_auction_seller_offer(added_seller_offer.id)
        return added_seller_offer
    else:
        logging.warning('EXAMPLE_AUCTION{auction_id} EXAMPLE_AUCTION seller offer is not valid'.format(auction_id=auction_id))


def format_seller_offer_to_save(added_seller_offer):
    '''
    Функция, приводящая торговое предложение продавца к виду для сохранения в form.
    :param added_seller_offer:
    :return: dict - торговое предложение продавца
    '''

    added_seller_offer = {
        'EXAMPLE_AUCTION': int(added_seller_offer['auction_id']),
        'lot_amount': int(added_seller_offer['count']),
        'start_price_per_tone': added_seller_offer['price_for_ton'],
    }

    return added_seller_offer


#TODO: ЛУЧШЕ ПЕРЕМЕСТИТЬ
def user_auctions_qs(user):
    from auction.models import Auction

    if user.has_perm('EXAMPLE_AUCTION.add_auction'):
        auctions = Auction.objects.filter(seller=user.id).order_by('start_bidding')

        for auction in auctions:
            status = auction.status
            if status == 'planning' or status == 'notValid':
                auctions = auctions.exclude(id=auction.id)

        return auctions

    user_auctions_ids = get_user_auctions(user)
    user_auctions = Auction.objects.none()
    for auction_id in user_auctions_ids:
        user_auctions = user_auctions | Auction.objects.filter(id=auction_id).order_by('start_bidding')
    return user_auctions


#TODO: ЛУЧШЕ ПЕРЕМЕСТИТЬ
def get_user_auctions(user):
    from auction.models import AuctionDeal

    auctions = set()
    deals = AuctionDeal.objects.filter(bet__client=user.id)
    for deal in deals:
        auctions.add(deal.bet.auction_id)

    return auctions


