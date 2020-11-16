import time
import logging
import copy
import redis
import threading
from threading import Thread
from datetime import timedelta
from django.template.loader import get_template
from django.db import models
from django.db.models import F, Sum, Max
from profile.models import Company
from django.conf import settings
from .forms import AuctionDealForm, AuctionBetForm, AuctionSellersOffersForm
from utils.time_customization.custom_time import current_datetime, replace_to_utc
from utils.iter_containers.dict_methods import remove_keys_from_dict
# from utils.notifications.send_file import group_send_html_on_emails
from authentication.user_methods import get_users_followed_for, get_dev_emails
# from utils.notifications.send_file import group_send_html_on_emails
from EXAMPLE_AUCTION.models import TradingType, TradingOperation, ShipmentMethods, ShipmentConditions, \
    BidLevel, PaymentTerms, ParticipationStatus, Document
from auction.validators import validate_decimals

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG,
                    filename=u'EXAMPLE_AUCTION.log')


class Auction(models.Model):
    type = models.ForeignKey(TradingType, models.DO_NOTHING, verbose_name="Операция")
    trading_operation = models.ForeignKey(TradingOperation, models.DO_NOTHING, db_column='trading_operation',
                                          verbose_name="Операция", default=1)
    polymer_id = models.IntegerField(verbose_name="Id полимера")
    polymer_shortcode = models.CharField(max_length=200, blank=True, verbose_name="Марка полимера")
    polymer_type = models.CharField(max_length=200, blank=True, verbose_name="Тип полимера")
    polymer_type_id = models.IntegerField(blank=True, verbose_name="Id типа полимера")
    polymer_plant = models.CharField(max_length=200, null=True, blank=True, verbose_name="Производитель полимера")
    polymer_plant_id = models.IntegerField(null=True, blank=True, verbose_name="Id производителя полимера")
    shipment_condition = models.ForeignKey(ShipmentConditions, models.DO_NOTHING, verbose_name="Условия при торгах")
    # shipment_method = models.ForeignKey(ShipmentMethods, models.DO_NOTHING, verbose_name="Методы доставки")
    delivery = models.CharField(max_length=200, verbose_name="Поставка")
    storage_location = models.CharField(max_length=200, verbose_name="Базис")
    lot_size = models.FloatField(validators=[validate_decimals], null=True, blank=True, verbose_name="Объем лота")
    payment_term = models.CharField(max_length=200, verbose_name="Способ оплаты")
    step = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Шаг торга")
    is_price_with_nds = models.BooleanField(default=False, blank=True, verbose_name="Цена на НДС")
    start_bidding = models.DateTimeField(verbose_name="Начало аукциона")
    end_bidding = models.DateTimeField(verbose_name="Конец аукциона")
    fixation_duration = models.IntegerField(default=60, verbose_name="Продолжительность фиксации")
    special_conditions = models.TextField(null=True, blank=True, verbose_name="Особые условия")
    level = models.ForeignKey(BidLevel, models.DO_NOTHING, verbose_name="Уровень заявки")
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, verbose_name="Продавец")
    published_datetime = models.DateTimeField(blank=True)
    is_finished = models.BooleanField(default=False, verbose_name="Аукцион закончен")
    is_template = models.BooleanField(default=False, blank=True, verbose_name="Типовой аукцион")
    template_name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Название шаблона")
    is_dev_bid = models.BooleanField(default=False, verbose_name="Для разработчиков")
    is_apply_for_participation = models.BooleanField(default=False, blank=True,
                                                     verbose_name='Есть ли подача заявок на участие')

    class Meta:
        verbose_name = "Аукцион"
        verbose_name_plural = "Аукционы"

    def __str__(self):
        return '{auction_type} аукцион № {auctionBidId}'.format(auction_type=self.type.name, auctionBidId=self.id)

    @property
    def status(self):
        # todo: поправить if
        '''
        Метод-свойство, возвращающий статус аукциона.
        :return: string - статус аукциона
        '''

        now = replace_to_utc(current_datetime())
        start_auction = replace_to_utc(self.start_bidding)
        end_auction = replace_to_utc(self.end_bidding)

        if now < start_auction:
            return 'planning'
        elif (now >= start_auction and now < end_auction) and (not self.is_finished):
            return 'active'
        elif (now >= end_auction and now.date() == end_auction.date()) or (
                        now.date() == end_auction.date() and self.is_finished):
            if self.have_bets:
                return 'finished_today'
        elif now >= end_auction or self.is_finished:
            if self.have_bets:
                return 'finished'
        else:
            return 'notValid'

    @property
    def have_bets(self):
        """
        Метод-свойство, возвращающий имеет ли данный аукцион ставки.
        :return: bool - есть ли ставки
        """

        num_auction_bets = AuctionBet.objects.filter(auction=self).count()
        return True if num_auction_bets else False

    @property
    def is_needed_continue(self):
        '''
        Метод-свойство, возращиющий ответ надо ли пролонгировать аукцион.
        :return: bool - надо ли пролонгировать аукцион
        '''

        return True if AuctionBet.objects.filter(end_fixation_datetime__gte=self.end_bidding).exists() else False

    @property
    def max_endFixationDatetime(self):
        '''
        Метод-свойство, возвращающий ставку с максимальным значением конца фиксации сделки.
        :return: объект - ставка
        '''

        return AuctionBet.objects.filter(end_fixation_datetime__gte=self.end_bidding). \
            aggregate(Max('end_fixation_datetime'))['end_fixation_datetime__max']

    @property
    def current_seller_offer(self):
        '''
        Метод, возвращающий текущее торговое предложение продавца по данному аукциону
        :return: объект - AuctionSellerOffer
        '''

        if self.type.name == 'Встречный':
            if AuctionSellerOffer.objects.filter(auction=self, is_closed_offer=False).exists():
                return AuctionSellerOffer.objects.get(auction=self, is_closed_offer=False)
            else:
                return None
        else:
            return AuctionSellerOffer.objects.get(auction=self)

    @property
    def num_free_lots(self):
        """
        Метод-свойство, возвращающий остаток лотов(нераспроданных).
        :return: int - остаток лотов аукциона
        """

        sum_lot_amount = self.get_sum_winning_deals_lot_amount()
        num_free_lots = self.current_seller_offer.lot_amount - sum_lot_amount
        return 0 if num_free_lots < 0 else num_free_lots

    @property
    def sum_reserved_lots(self):
        '''
        Метод-свойство, возвращающий количество зарезервированных лотов.
        :return: int - количество зарезервированных лотов
        '''

        start_price_per_tone = self.current_seller_offer.start_price_per_tone
        sum_reserved_lots = \
            AuctionBet.objects.filter(auction=self).exclude(is_winning_bet=True) \
                .exclude(is_increased_bet=True) \
                .exclude(is_deleted_bet=True) \
                .exclude(bet_price_per_tone__lt=start_price_per_tone) \
                .aggregate(sum_reserved_lots=Sum('lot_amount'))['sum_reserved_lots']

        return sum_reserved_lots if sum_reserved_lots else 0

    def save(self, is_updated=False, *args, **kwargs):
        super(Auction, self).save(*args, **kwargs)
        if not is_updated: self.put_to_notifications_queue()

    def delete(self, *args, **kwargs):
        if AuctionBet.objects.filter(auction=self.pk).exists():
            raise Exception('This EXAMPLE_AUCTION has bets, therefore you can not delete this.')

        auction_copy = copy.copy(self)

        thread = Thread(target=self.send_cancel_trade_offer_notification, args=(self.get_display_data(),))
        thread.start()

        if self.type.name == 'Классический':
            if AuctionSellerOffer.objects.filter(auction=self).exists():
                AuctionSellerOffer.objects.filter(auction=self).delete()

        super().delete(*args, **kwargs)

        return auction_copy

    def save_seller_offer(self, seller_offer_data):
        seller_offer_data['EXAMPLE_AUCTION'] = self.id
        form = AuctionSellersOffersForm(seller_offer_data)
        if form.is_valid():
            seller_offer = form.save()
            return seller_offer
        else:
            logging.error(form.errors)
            self.delete()
            return False

    def put_to_notifications_queue(self):
        """
        Метод, отвечающий за добавление аукциона в очередь отправки уведомлений
        :return:
        """
        try:
            r = redis.Redis()
            auction_notifications_set = r.smembers("auction_notifications")
            if auction_notifications_set:
                auction_notifications_list = [int(notify.decode('utf8')) for notify in auction_notifications_set]
                auction_notifications_list.append(self.id)
            else:
                auction_notifications_list = [self.id]
            r.sadd("auction_notifications", *auction_notifications_list)
        except Exception as ex:
            logging.error(ex)

    def check_end_to_continue(self, added_bet):
        '''
        Метод, проверяющий конец аукциона. Необходим для пролонгирования аукциона.
        :param added_bet:
        :return:
        '''

        if self.end_bidding < added_bet.end_fixation_datetime:
            self.end_bidding = added_bet.end_fixation_datetime
            self.save(is_updated=True)

            logging.info('Auction{auction_id}: Change Auction endAuction'.format(auction_id=self.id))

    def finish(self):
        '''
        Метод, завершающий аукцион.
        :return:
        '''
        logging.info('Auction{auction_id}: Finish Auction'.format(auction_id=self.id))

        self.is_finished = True
        self.end_bidding = current_datetime()
        self.save(is_updated=True)
        if self.have_bets: self.send_bidding_protocols()

    def get_sum_winning_deals_lot_amount(self):
        """
        Метод, возвращающий сумму количества лотов сделок по данному ...(выигравших ставок).
        :return: int - сумма количества лотов сделок
        """

        seller_offer = self.current_seller_offer
        sum_lot_amount = AuctionDeal.objects.filter(seller_offer=seller_offer). \
            aggregate(sum_lot_amount=Sum('lot_amount'))['sum_lot_amount']

        return sum_lot_amount if sum_lot_amount else 0

    def get_all_bets(self):
        """
        Метод, возвращающий все ставки для определенного аукциона
        :return:
        """

        return AuctionBet.objects.filter(auction=self)

    def get_user_bets(self, user):
        """
         Метод, возвращающий все ставки для определенного юзера
        :return:
        """

        return AuctionBet.objects.filter(auction=self, client=user)

    def get_user_active_bets(self, user):
        """
        Метод, возвращающий все акттивные ставки юзера
        :param user:
        :return:
        """

        user_bets = self.get_user_bets(user).exclude(id__in=self.get_fixation_bets_ids_list()) \
            .exclude(is_winning_bet=True) \
            .exclude(is_increased_bet=True) \
            .exclude(is_deleted_bet=True) \
            .order_by('-bet_price_per_tone', 'published_datetime')
        return user_bets

    def get_current_bets_for_auction(self):
        '''
        Метод, возвращающий текущий ставки(ставки, которые не были удалены, инкрементированы пользователем,
        а также ставки не являющиеся выйгрышными)
        :return: queryset - с текущими ставками
        '''

        bets = self.get_all_bets().exclude(is_winning_bet=True) \
            .exclude(is_increased_bet=True) \
            .exclude(is_deleted_bet=True) \
            .order_by('-bet_price_per_tone', 'published_datetime')
        return bets

    def get_fixation_bets_list(self):
        """
        Метод, возвращающий ставки, находящиеся в области фиксации.
        :return: лист - ставки в области фиксации
        """

        fixation_bets_list = []
        sum_lot_amount = 0  # сумма количества лотов ставок аукциона
        all_bets = self.get_current_bets_for_auction()
        for bet in all_bets:
            if not bet.is_winning_bet and bet.bet_price_per_tone >= self.current_seller_offer.start_price_per_tone:
                sum_lot_amount += bet.lot_amount
                fixation_bets_list.append(bet)
                if sum_lot_amount >= self.num_free_lots:
                    break

        return fixation_bets_list

    def get_fixation_bets_ids_list(self):
        """
        Метод, возвращающий список ids ставок находящихся в области фиксации.
        :return: список ids ставок находящихся в области фиксации
        """

        if self.type.name == 'Голландский':
            current_price_per_tone = self.current_seller_offer.middle_price_per_tone
        else:
            current_price_per_tone = self.current_seller_offer.start_price_per_tone

        fixation_bets_ids_list = []
        sum_lot_amount = 0  # сумма количества лотов ставок аукциона
        all_bets = self.get_current_bets_for_auction()
        for bet in all_bets:
            if not bet.is_winning_bet and bet.bet_price_per_tone >= current_price_per_tone:
                sum_lot_amount += bet.lot_amount
                fixation_bets_ids_list.append(bet.id)
                if sum_lot_amount >= self.num_free_lots:
                    break

        return fixation_bets_ids_list

    def set_fixation_time_to_bets(self, fixation_bets_list):
        '''
        Метод, устанавливающий время конца фиксации сделки для нескольких ставок.
        :param fixation_bets_list: лист - ставки
        :return:
        '''

        end_fixation_datetime = current_datetime() + timedelta(seconds=self.fixation_duration)
        auction_bets = AuctionBet.objects.filter(auction=self, id__in=fixation_bets_list)
        for bet in auction_bets:
            bet.end_fixation_datetime = end_fixation_datetime
            bet.save()

        logging.debug(
            'Auction{auction_id}: bets list to set fixation time {end_fixation_datetime} to {fixation_bets_list}'
                .format(auction_id=self.id,
                        end_fixation_datetime=end_fixation_datetime,
                        fixation_bets_list=fixation_bets_list))

    def make_deals_with(self, added_bet_id, seller_offer):
        """
        Метод, заключающий сделки для ставок с одинаковым временнем фиксации.
        :param added_bet_id: id - ставки
        :return:
        """

        bet = AuctionBet.objects.get(id=added_bet_id)
        fixation_bets_ids = self.get_fixation_bets_ids_list()

        fixation_bets = AuctionBet.objects.filter(auction=bet.auction,
                                                  end_fixation_datetime=bet.end_fixation_datetime,
                                                  id__in=fixation_bets_ids). \
            order_by('-bet_price_per_tone', 'published_datetime')

        fix_deals = []
        for bet in fixation_bets:
            deal = bet.make_deal(seller_offer)
            if deal: fix_deals.append(deal)

        logging.debug('Auction{auction_id}: Make deal with this bets {bets}'
                      .format(auction_id=bet.auction.id, bets=fixation_bets.values()))

        return fix_deals

    def get_client_deals(self, user):
        """
        Метод, возвращающаий все сделки аукциона для данного клиента, отсортированные по дате заключения сделки.
        :param user: id клиента/объект клиента
        :return: список объектов-сделки
        """

        return AuctionDeal.objects.filter(bet__auction=self, bet__client=user).order_by('published_datetime')

    def get_all_deals(self):
        """
        Метод, возвращающаий все сделки аукциона, отсортированные по дате заключения сделки.
        :return: список объектов-сделки
        """

        return AuctionDeal.objects.filter(bet__auction=self).order_by('published_datetime')

    def get_deals_for_user(self, user):
        if self.seller == user or user.has_perm('authentication.can_view_all_data'):
            client_deals = [deal.get_display_data(user) for deal in self.get_all_deals()]
        else:
            client_deals = [deal.get_display_data(None) for deal in self.get_client_deals(user)]

        return client_deals

    def get_display_data(self):
        '''
        Метод, возвращающий все свойства аукциона.
        :return: словарь - все свойства аукциона
        '''

        if self.type.name == 'Встречный':
            lot_amount, total_amount, start_price_per_tone, middle_price_per_tone, stop_price_per_tone = None, None, None, None, None
        else:
            stop_price_per_tone = self.current_seller_offer.stop_price_per_tone if self.type.name == 'Голландский' else None
            lot_amount = self.current_seller_offer.lot_amount
            total_amount = self.current_seller_offer.total_amount
            start_price_per_tone = self.current_seller_offer.start_price_per_tone
            middle_price_per_tone = self.current_seller_offer.middle_price_per_tone
            stop_price_per_tone = self.current_seller_offer.stop_price_per_tone

        if self.status in ['finished', 'finished_today', 'notValid']:
            min_price_per_tone = ''
            start_price_per_tone = ''
            middle_price_per_tone = ''

        return {'auction_id': self.id,
                'status': self.status,
                'type': self.type.name,
                'type_id': self.type.id,
                'level_id': self.level.id,
                'level_name': self.level.name,
                'trading_operation': self.trading_operation.name,
                'trading_operation_id': self.trading_operation.id,
                'polymer_id': self.polymer_id,
                'polymer_type': self.polymer_type,
                'polymer_type_id': self.polymer_type_id,
                'polymer_shortcode': self.polymer_shortcode,
                'polymer_plant': self.polymer_plant,
                'start_bidding': self.start_bidding,
                'end_bidding': self.end_bidding,
                'fixation_duration': self.fixation_duration,
                'special_conditions': self.special_conditions,
                'published_datetime': self.published_datetime,
                'shipment_condition': self.shipment_condition.name,
                'shipment_condition_id': self.shipment_condition.id,
                'payment_term': self.payment_term,
                'delivery': self.delivery,
                'lot_size': self.lot_size,
                'lot_amount': lot_amount,
                'total_amount': total_amount,
                'start_price_per_tone': start_price_per_tone,
                'middle_price_per_tone': middle_price_per_tone,
                'stop_price_per_tone': stop_price_per_tone,
                'is_price_with_nds': self.is_price_with_nds,
                'step': self.step,
                'storage_location': self.storage_location,
                'seller_id': self.seller.id,
                'seller_username': self.seller.username,
                'seller_email': self.seller.email,
                'seller__company_full_name': self.seller.company.full_name,
                'seller__company_short_name': self.seller.company.short_name,
                'is_apply_for_participation': self.is_apply_for_participation,
                }

    def get_auction_session_data(self, user, fixation_bets=None):
        """
        Метод, взависимости от типа аукциона возвращает информацию о торговой сессии
        """

        if self.type.name == 'Голландский':
            return self.get_holland_auction_session_data(user, fixation_bets)
        elif self.type.name == 'Встречный':
            return self.get_counter_auction_session_data(user, fixation_bets)
        else:
            return self.get_typical_auction_session_data(user, fixation_bets)

    def get_counter_auction_session_data(self, user, fixation_bets=None):
        """
        Метод, возвращающий всю информацию о текущей сессии встречного аукциона.
        :param user:
        :param fixation_bets:
        :return:
        """

        all_bets = [bet.get_display_data(user) for bet in self.get_current_bets_for_auction()]
        client_deals = self.get_deals_for_user(user)
        data = {
            'all_bets': all_bets,
            'client_deals': client_deals,
            'now_datetime': current_datetime(),
            'end_bidding': self.end_bidding,
        }

        if not self.current_seller_offer or self.current_seller_offer.is_closed_offer:
            extra_data = {
                'current_seller_offer': None,
                'num_free_lots': 'Не указано',
                'num_reserved_lots': 'Не указано'
            }
        else:
            num_reserved_lots = self.num_free_lots if self.sum_reserved_lots > self.num_free_lots else self.sum_reserved_lots
            extra_data = {
                'current_seller_offer': {'lot_amount': self.current_seller_offer.lot_amount,
                                         'start_price_per_tone': self.current_seller_offer.start_price_per_tone
                                         },
                'fixation_bets_ids_list': self.get_fixation_bets_ids_list(),
                'num_free_lots': self.num_free_lots,
                'num_reserved_lots': num_reserved_lots,
            }

        return data.update(extra_data)

    def get_typical_auction_session_data(self, user, fixation_bets=None):
        """
        Метод, возвращающий всю информацию о текущей сессии классического аукциона.
        :param user:
        :param fixation_bets:
        :return:
        """

        all_bets = [bet.get_display_data(user) for bet in self.get_current_bets_for_auction()]
        client_deals = self.get_deals_for_user(user)
        num_reserved_lots = self.num_free_lots if self.sum_reserved_lots > self.num_free_lots else self.sum_reserved_lots

        data = {
            'current_seller_offer': {'lot_amount': self.current_seller_offer.lot_amount,
                                     'start_price_per_tone': self.current_seller_offer.start_price_per_tone
                                     },
            'all_bets': all_bets,
            'fixation_bets_ids_list': self.get_fixation_bets_ids_list(),
            'client_deals': client_deals,
            'num_free_lots': self.num_free_lots,
            'num_reserved_lots': num_reserved_lots,
            'now_datetime': current_datetime(),
            'end_bidding': self.end_bidding
        }
        return data

    def get_holland_auction_session_data(self, user, fixation_bets=None):
        '''
        Метод, возвращающий всю информацию о текущей сессии голландского аукциона.
        :param user:
        :param fixation_bets:
        :return:
        '''

        fixation_bets = [bet.get_display_data(user) for bet in
                         AuctionBet.objects.filter(id__in=self.get_fixation_bets_ids_list())]

        user_bets = [bet.get_display_data(user) for bet in self.get_user_active_bets(user)]
        all_bets = fixation_bets + user_bets
        client_deals = self.get_deals_for_user(user)
        num_reserved_lots = self.num_free_lots if self.sum_reserved_lots > self.num_free_lots else self.sum_reserved_lots
        data = {
            'middle_price_per_tone': self.current_seller_offer.middle_price_per_tone,
            'all_bets': all_bets,
            'fixation_bets_ids_list': self.get_fixation_bets_ids_list(),
            'client_deals': client_deals,
            'num_free_lots': self.num_free_lots,
            'num_reserved_lots': num_reserved_lots,
            'now_datetime': current_datetime(),
            'end_bidding': self.end_bidding
        }

        return data

    def send_notifications(self):
        Thread(target=self.send_create_trade_offer_notification).start()
        threading.Timer((self.start_bidding - current_datetime()).seconds,
                        self.send_start_trade_offer_notification).start()

        if self.type.name == 'Голландский':
            timedelta_d = (self.start_bidding - current_datetime()).seconds
            threading.Timer(timedelta_d, self.start_reduce_min_price_per_tone_timer).start()

    def send_create_trade_offer_notification(self, defined_users_list=None):
        logging.debug('Auction{auction_id}: send create_trade_offer_notification'.format(auction_id=self.id))
        from utils.notifications.send_file import group_send_html_on_emails

        filter_params = {'creating_auction_notification': True}
        data = self.get_display_data()

        if self.level.name == 'Открытые торги':
            users_emails = get_users_followed_for(filter_params, data['polymer_id'])

        logging.debug(
            'Auction{auction_id}: send create_trade_offer_notification to {users_emails}'.format(auction_id=self.id,
                                                                                                 users_emails=users_emails))

        htmly = get_template('email_messages/create_auction_message.html')

        html_content = htmly.render(data)

        if defined_users_list:
            group_send_html_on_emails('', '', html_content, defined_users_list)
        else:
            group_send_html_on_emails('Торги №{auction_id}'.format(auction_id=self.id), '', html_content, users_emails)

    def send_start_trade_offer_notification(self):
        from utils.notifications.send_file import group_send_html_on_emails

        filter_params = {'starting_auction_notification': True}
        data = self.get_display_data()

        users_emails = get_users_followed_for(filter_params, data['polymer_id'])

        logging.debug(
            'Auction{auction_id}: send start_trade_offer_notification to {users_emails}'.format(auction_id=self.id,
                                                                                                users_emails=users_emails))

        if settings.ALLOWED_HOSTS:
            data['domain'] = settings.ALLOWED_HOSTS[0]
        else:
            data['domain'] = '127.0.0.1:8000'

        htmly = get_template('email_messages/start_auction_message.html')
        html_content = htmly.render(data)

        group_send_html_on_emails('Торги №{auction_id}'.format(auction_id=self.id), '', html_content, users_emails)

    def send_cancel_trade_offer_notification(self, data):
        from utils.notifications.send_file import group_send_html_on_emails

        filter_params = {'cancel_auction_notification': True}

        keys_to_remove = ['lot_amount', 'total_amount', 'special_conditions', 'step', 'lot_size', 'payment_term']

        remove_keys_from_dict(keys_to_remove, data)

        users_emails = get_users_followed_for(filter_params, data['polymer_id'])

        logging.debug(
            'Auction{auction_id}: send cancel_trade_offer_notification to {users_emails}'.format(auction_id=self.id,
                                                                                                 users_emails=users_emails))

        htmly = get_template('email_messages/cancel_auction_message.html')
        html_content = htmly.render(data)

        group_send_html_on_emails('Торги №{auction_id}'.format(auction_id=data['auction_id']), '', html_content,
                                  users_emails)

    def start_reduce_min_price_per_tone_timer(self):
        """
        Метод, контролирующий запуск/окончание уменьшения цены
        :return:
        """

        reduce_flag = True
        while reduce_flag:
            time.sleep(self.fixation_duration)
            reduce_flag = self.reduce_min_price_per_tone()

    def reduce_min_price_per_tone(self):
        """
        Метод, уменьшающий текущую цену
        :return:
        """

        current_seller_offer = self.current_seller_offer
        auction = Auction.objects.get(id=self.id)
        if current_seller_offer.middle_price_per_tone - self.step >= current_seller_offer.stop_price_per_tone \
                and not auction.is_finished:
            current_seller_offer.middle_price_per_tone = current_seller_offer.middle_price_per_tone - self.step
            current_seller_offer.save()
            return True
        else:
            return False

    def send_bidding_protocols(self):
        from utils.notifications.send_file import send_bidding_protocol_for_deal

        data = self.get_display_data()

        logging.info('EXAMPLE_AUCTION{auction_id}: sending bidding protocols'.format(auction_id=self.id))
        deals = AuctionDeal.objects.filter(bet__auction=self)

        htmly = get_template('email_messages/bidding_protocol_message.html')

        html_content = htmly.render(data)

        for deal in deals:
            Thread(target=send_bidding_protocol_for_deal,
                   args=(deal, 'Торги №{auction_id}'.format(auction_id=self.id), html_content)).start()


class AuctionParticipationOrder(models.Model):
    auction = models.ForeignKey(Auction, models.DO_NOTHING, verbose_name="Аукцион")
    company = models.ForeignKey(Company, models.DO_NOTHING, verbose_name="Компания")
    participation_status = models.ForeignKey(ParticipationStatus, models.DO_NOTHING, default=2,
                                             verbose_name="Статус участия")

    class Meta:
        unique_together = [['EXAMPLE_AUCTION', 'company']]


class AuctionSellerOffer(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    lot_amount = models.IntegerField(verbose_name="Количество лотов")
    total_amount = models.FloatField(validators=[validate_decimals], null=True, blank=True,
                                     verbose_name="Общее количество")
    start_price_per_tone = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Стартовая ценна за тонну")
    middle_price_per_tone = models.DecimalField(max_digits=9, decimal_places=2, blank=True,
                                                verbose_name="Стартовая ценна за тонну")
    stop_price_per_tone = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True,
                                              verbose_name="Стоп ценна за тонну")
    published_datetime = models.DateTimeField(blank=True)
    is_closed_offer = models.BooleanField(default=False, verbose_name="Предложение закончено")
    current_max_bet = models.IntegerField(default=0)

    def change_current_max_bet(self, max_bet_id):
        self.current_max_bet = max_bet_id
        self.save()

    def close(self):
        self.is_closed_offer = True
        self.save()


class AuctionBet(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    lot_amount = models.IntegerField()
    total_amount = models.FloatField(validators=[validate_decimals], null=True, blank=True,
                                     verbose_name="Общее количество")
    bet_price_per_tone = models.DecimalField(max_digits=9, decimal_places=2)
    total_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True)
    is_winning_bet = models.BooleanField(default=False)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)
    published_datetime = models.DateTimeField(blank=True)
    end_fixation_datetime = models.DateTimeField(blank=True, null=True)
    is_increased_bet = models.BooleanField(default=False)
    is_deleted_bet = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Ставка"
        verbose_name_plural = "Ставки"

    @property
    def is_middle_in_fixation_bets(self):
        fixation_bets = self.auction.get_fixation_bets_list()
        for bet in fixation_bets:
            if self.bet_price_per_tone > bet.bet_price_per_tone and self.published_datetime > bet.published_datetime:
                return True

        return False

    def set_end_fixation_datetime(self, end_fixation_datetime):
        self.end_fixation_datetime = end_fixation_datetime
        self.save()

    def set_is_increased_bet(self):
        self.is_increased_bet = True
        self.end_fixation_datetime = None
        self.save()

    def set_is_deleted_bet(self):
        self.is_deleted_bet = True
        self.end_fixation_datetime = None
        self.save()

    def get_secret_display_data(self, user):
        if user:
            if self.client == user or user.user.has_perm('authentication.can_view_all_data'):
                return {'client_id': self.client.id,
                        'client_first_name': self.client.first_name,
                        'client_last_name': self.client.last_name}

        return {}

    def get_data(self, user=None):
        data = {'id': self.id,
                'auction_id': self.auction.id,
                'lot_amount': self.lot_amount,
                'total_amount': self.total_amount,
                'bet_price_per_tone': self.bet_price_per_tone,
                'total_price': self.total_price,
                'is_increased_bet': self.is_increased_bet,
                'is_winning_bet': self.is_winning_bet,
                'published_datetime': self.published_datetime,
                'end_fixation_datetime': self.end_fixation_datetime,
                }
        data.update(self.get_secret_display_data(user))
        return data

    def make_deal(self, seller_offer):
        """
        Функция, заключающая сделку. Создает новую сделку и отмечает флагом выйгрышную ставку.
        :param bet: объект-ставки
        :return:
        """

        data = {
            'bet': self.id,
            'lot_amount': self.lot_amount,
            'seller_offer': seller_offer.id,
        }

        if self.auction.num_free_lots:
            if self.auction.num_free_lots < data['lot_amount']:
                diff_lot_amount = data['lot_amount'] - self.auction.num_free_lots
                data['lot_amount'] = self.auction.num_free_lots

                if self.auction.type.name == 'Встречный':
                    bet_data = {'EXAMPLE_AUCTION': self.auction.id,
                                'lot_amount': diff_lot_amount,
                                'bet_price_per_tone': self.bet_price_per_tone,
                                'client': self.client.id, }

                    bet_form = AuctionBetForm(bet_data)
                    if bet_form.is_valid():
                        bet_form.save()
                    else:
                        logging.error(
                            'Auction{auction_id}: {errors}'.format(auction_id=self.auction_id, errors=bet_form.errors))

        deal_form = AuctionDealForm(data)
        if deal_form.is_valid():
            deal = deal_form.save()
            self.is_winning_bet = True
            self.save()
            return deal
        else:
            return None


class AuctionDeal(models.Model):
    seller_offer = models.ForeignKey(AuctionSellerOffer, on_delete=models.CASCADE)
    bet = models.ForeignKey(AuctionBet, on_delete=models.CASCADE)
    lot_amount = models.IntegerField()
    total_amount = models.FloatField(validators=[validate_decimals], null=True, blank=True,
                                     verbose_name="Общее количество")
    total_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True)
    # file_path = models.FileField(upload_to='bidding_protocols/auctions/pdfs/', null=True, blank=True, verbose_name="Файл ")
    published_datetime = models.DateTimeField(blank=True)

    class Meta:
        verbose_name = "Сделка"
        verbose_name_plural = "Сделки"

    def __str__(self):
        return 'Сделка №{deal_id}; {seller_short_name} - {client_short_name}; {auction_type} аукцион № {auctionBidId}' \
            .format(auction_type=self.bet.auction.type.name,
                    auctionBidId=self.bet.auction.id,
                    deal_id=self.id,
                    seller_short_name=self.bet.auction.seller.company.short_name,
                    client_short_name=self.bet.client.company.short_name,
                    )

    def added_now(self, user):
        if self.bet.id in self.bet.auction.get_fixation_bets_ids_list():
            if user:
                if user.has_perm('authentication.can_view_all_data') or user == self.bet.auction.seller:
                    return {'added_now': False}
                else:
                    return {'added_now': True}
            else:
                return {'added_now': True}

        return {}

    def get_secret_display_data(self, user):
        if user:
            if user.has_perm('authentication.can_view_all_data'):
                return {'client_id': self.bet.client,
                        'client_first_name': self.bet.client.first_name,
                        'client_last_name': self.bet.client.last_name,
                        'client_email': self.bet.client.email,
                        'client_company_id': self.bet.client.company.id,
                        'client_company_short_name': self.bet.client.company.short_name,
                        'client_company_full_name': self.bet.client.company.full_name}

        return {}

    def get_display_data(self, user=None):
        data = {'id': self.id,
                'bet_id': self.bet.id,
                'lot_amount': self.lot_amount,
                'total_price': self.total_price,
                'total_amount': self.total_amount,
                'bet_price_per_tone': self.bet.bet_price_per_tone,
                'published_datetime': self.published_datetime
                }
        secret_data = self.get_secret_display_data(user).update(self.added_now(user))
        return data.update(secret_data)
