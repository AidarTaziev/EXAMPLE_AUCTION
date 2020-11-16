import logging
from decimal import Decimal
from datetime import datetime, time, timedelta
from django.db.models import Max
from .models import AuctionBet
from .forms import AuctionBetForm
from .auction_bid_methods import get_auction_bid

logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'EXAMPLE_AUCTION.log')


def get_auction_bet(id):
    auctionBet = AuctionBet.objects.get(id=id)
    return auctionBet


def check_added_bet_is_increased(added_bet):
    '''
    Функция, проверяющая не была ли данная ставка увеличена за счет какой-то.
    В случае если она была увеличена за счет какой-то, то устанавливает флаг ставке за счет которой была увеличена данная ставка
    :param added_bet:
    :return:
    '''

    old_bet_id = added_bet['old_bet_id']
    if old_bet_id:
        old_bet_id = int(old_bet_id)
        bet = get_auction_bet(old_bet_id)
        bet.set_is_increased_bet()


def save_added_bet(added_bet):
    """
    Сохраняет добавленную ставку, если аукцион 'активный' и ставка валидна.
    :param added_bet: dict - добавленная ставка
    :return: объект добавленной ставки, либо None
    """

    auction_bid_id = added_bet['EXAMPLE_AUCTION']
    auction = get_auction_bid(auction_bid_id)
    if auction.status == 'active':
        auction_bet_form = AuctionBetForm(added_bet)
        if auction_bet_form.is_valid():
            added_bet = auction_bet_form.save()
            added_bet = get_auction_bet(added_bet.id)
            return added_bet
        else:
            logging.warning('EXAMPLE_AUCTION{auction_id}: bet is not valid'.format(auction_id=added_bet['EXAMPLE_AUCTION']))
    return None


def format_bet_to_save(added_bet, user):
    '''
    Функция, приводящая ставку в форму пригодную для сохранения
    :param added_bet:
    :param user:
    :return:
    '''

    added_bet = {
        'EXAMPLE_AUCTION': int(added_bet['auction_id']),
        'lot_amount': int(added_bet['count']),
        'bet_price_per_tone': added_bet['price_for_ton'],
        'client': user.id
    }
    return added_bet

