from auction.auction_bid_methods import get_auction_bid, user_auctions_qs
from tender.tender_methods.tender_list import get_user_tender_qs
from tender import models
import datetime


def deals_date_separation(user, date_start=None, date_end=None):
    auctions = user_auctions_qs(user)
    tenders = get_user_tender_qs(user)

    date_separation = set(auctions.dates('start_bidding', 'day').reverse()) | set(tenders.dates('start_bidding', 'day').reverse())


    result = bidding_date_separation(auctions, tenders, user, date_separation)

    return result


def bidding_date_separation(auctions, tenders, user, date_separation):
    result = []
    block_counter = 0
    for date in date_separation:
        print(date)
        temp = {}
        temp['date'] = date
        temp['block_id'] = block_counter
        block_counter += 1

        day_begin = datetime.datetime.combine(date, datetime.time(0, 0, 0, 0))
        day_end = datetime.datetime.combine(date, datetime.time(23, 59, 59, 0))

        date_tenders = tenders.filter(start_bidding__range=(day_begin, day_end))
        date_auctions = auctions.filter(start_bidding__range=(day_begin, day_end))

        temp['tenders'] = create_object_to_render(date_tenders, user)
        temp['auctions'] = create_object_to_render(date_auctions, user)

        result.append(temp)

    return result


def create_object_to_render(biddings, user):

    result = []
    for bidding in biddings:

        bid_str = str(bidding)
        if is_seller(user) or bidding.seller == user:
            deals = bidding.get_all_deals()
        else:
            deals = bidding.get_client_deals(user)

        if deals:
            result.append({
                'id': bidding.id,
                'bid': bid_str,
                'deals': deals,
            })

    return result


def is_seller(user):
    return user.has_perm('authentication.can_view_all_data') or \
           user.has_perm('EXAMPLE_AUCTION.add_auction')
