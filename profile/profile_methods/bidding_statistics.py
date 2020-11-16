from auction.auction_bid_methods import user_auctions_qs


def auction_info(users):
    """
    Сбор статистики пользователей, сюда можно передать QuerySet пользователя
    """
    company_auctions_set = set()
    company_win_auctions_set = set()
    company_deals_count = 0

    for user in users:
        user_auctions = user_auctions_qs(user)

        for auction in user_auctions:
            company_auctions_set.add(auction.id)
            deals = auction.get_client_deals(user=user.id)
            if deals:
                company_win_auctions_set.add(auction.id)
                company_deals_count += 1


    auctions_count = len(company_auctions_set)
    win_auctions_count = len(company_win_auctions_set)
    return {
        'all': auctions_count,
        'lost': auctions_count - win_auctions_count,
        'deals': company_deals_count,
    }
