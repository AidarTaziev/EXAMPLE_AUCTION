from EXAMPLE_AUCTION.models import *


def get_all_selects_data():
    """
    Возвращает заполненый словарь со значениями фильтров - основной страницы поиска
    :return: словарь со значениями фильтров
    """

    FILTERS_TABLES = {
        "trading_operations": TradingOperation,
        "shipment_methods": ShipmentMethods,
        "payment_terms": PaymentTerms,
        "auction_levels": BidLevel,
        "auction_types": TradingType,
    }

    data = {}
    for filter, table in FILTERS_TABLES.items():
        table_rows = table.objects.all().order_by('name').values()
        data[filter]= table_rows

    return data


def get_catalogues_data():
    data = get_all_selects_data()
    data['polymers'] = get_all_polymers_short_info()
    data['shipment_conditions'] = ShipmentConditions.objects.all().order_by('id')
    data['auctions_templates'] = Auction.objects.filter(seller=request.user, is_template=True).order_by('id')

    return data