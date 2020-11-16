import json
import copy
import logging
# import aioredis
# from aredis import StrictRedis
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.httpclient
from datetime import timedelta
from utils.time_customization.custom_time import current_datetime
from auction.auction_bid_methods import get_auction_bid
from authentication.user_methods import get_user_for_cookie
from auction.auction_bet_methods import get_auction_bet


logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'auction.log')


class BaseAuctionWebSocket(tornado.websocket.WebSocketHandler):
    waiters = {}
    auction_end_callback = {}

    def check_origin(self, origin):
        return True

    async def open(self, auctionId):
        self.auction = get_auction_bid(auctionId)
        self.saller_offer = self.auction.current_seller_offer
        self.session_name = 'auction%d' % self.auction.id
        self.clients_group_name = '%d:clients' % self.auction.id
        self.user = get_user_for_cookie(self.get_cookie("sessionid"))

        self.check_auction_status()
        self.set_auction_callback()
        self.add_user_to_waiters()
        self.send_session_data_to_user()

    def check_auction_status(self):
        """
        Метод проверяет, проверяет статус аукциона и отправляет сообщение об окончании в случае если аукцион не валидный
        """

        if self.auction.status != 'active':
            self.write_message(json.dumps({'auction_is_finished': True}, ensure_ascii=False, default=str))
            self.close()

    def set_auction_callback(self):
        """
        Метод, устанавливающий коллбэк окончания сессии аукциона
        """

        if self.session_name not in self.auction_end_callback:
            loop = tornado.ioloop.IOLoop.current()
            timedelta_d = self.auction.end_bidding - current_datetime()
            callback = loop.add_timeout(timedelta_d, self.check_auction_end, self.auction.id, self.auction.end_bidding)
            self.auction_end_callback[self.session_name] = callback

    def add_user_to_waiters(self):
        """
        Метод, добавляющий пользователя в группу аукциона (ожидающих соообщений)
        """

        if self.clients_group_name not in self.waiters.keys():
            self.waiters[self.clients_group_name] = set()
        self.waiters[self.clients_group_name].add((self, self.user))

    def send_session_data_to_user(self):
        """
        Метод, отвечающий за отправку данных сессии аукцина опредленному юзеру
        """

        data = self.auction.get_auction_session_data(self.user)
        self.write_message(json.dumps(data, ensure_ascii=False, default=str))


    def bet_fixation_timeout_callback(self, added_bet):
        """
        Метод, отвечающий за проверяку находится ли ставка в области фиксации,
        не увеличивалось ли время фиксации и в зависимости от этого он
        1) либо заключает сделку
        2) либо запускает новый таймер для ставки
        3) либо отбрасывает ставку(в случае если она не в области фиксации)
        :param added_bet: объект ставки - ставка переданная на момент запуска таймера
        :return:
        """

        fixation_bets_ids = self.auction.get_fixation_bets_ids_list()
        current_added_bet = get_auction_bet(id=added_bet.id)#объект добавленной ставки в текущей версии(тк могло измениться время фиксации)

        if added_bet.id in fixation_bets_ids:
            if added_bet.end_fixation_datetime.strftime(
                    "%Y.%m.%d %H:%M:%S") == current_added_bet.end_fixation_datetime.strftime("%Y.%m.%d %H:%M:%S"):
                if self.auction.num_free_lots:
                    self.auction.make_deals_with(added_bet.id, self.auction.current_seller_offer)
                    self.check_free_lots()
                    self.group_send_auction_session_data(fixation_bets_ids)
                else:
                    self.write_message(json.dumps({'auction_is_finished': True}, ensure_ascii=False, default=str))
                    self.close()
            elif added_bet.end_fixation_datetime < current_added_bet.end_fixation_datetime:
                timedelta_d = current_added_bet.end_fixation_datetime - added_bet.end_fixation_datetime
                loop = tornado.ioloop.IOLoop.current()
                loop.add_timeout(timedelta_d, self.bet_fixation_timeout_callback, current_added_bet)

    def group_send_added_bet(self, added_bet):
        """
        Метод, рассылоющий всем пользователям/покупателям (ожидающим) аукционна инфорацию о добавленной ставке
        """

        for waiter in self.waiters[self.clients_group_name]:
            cur_added_bet = copy.copy(added_bet)
            try:
                data = self.auction.get_auction_session_data(waiter[1])
                data['added_bet'] = cur_added_bet.get_data()
                if waiter[1].id != added_bet.client.id:
                    cur_added_bet.client_id = None
                    data['added_bet']['client_id'] = None

                waiter[0].write_message(json.dumps(data, ensure_ascii=False, default=str))
            except Exception as ex:
                logging.warning('Auction{auction_id}: Send to user exception - {ex}'.format(auction_id=self.auction.id, ex=ex))

    def group_send(self, auctionId, message):
        """
        Метод, рассылоющий всем пользователям/покупателям (ожидающим) аукционна заданную информацию
        """

        for waiter in self.waiters[self.clients_group_name]:
            try:
                waiter[0].write_message(message)
            except Exception as ex:
                logging.warning('auction{auction_id}: Send to user exception - {ex}'.format(auction_id=self.auction.id, ex=ex))

    def group_send_auction_session_data(self, fixation_bets=None):
        """
        Метод, рассылоющий всем пользователям/покупателям (ожидающим) аукционна текущую информацию об аукционе
        """

        for waiter in self.waiters[self.clients_group_name]:
            try:
                data = self.auction.get_auction_session_data(waiter[1], fixation_bets)
                waiter[0].write_message(json.dumps(data, ensure_ascii=False, default=str))
            except Exception as ex:
                logging.warning('Auction{auction_id}: Send to user exception - {ex}'.format(auction_id=self.auction.id, ex=ex))

    def check_free_lots(self):
        """
        Метод, проверяющий свободные лоты, в случае если их нет, то закрывает предложение продавца (делает его неактивным)
        """

        if not self.auction.num_free_lots:
            self.auction.current_seller_offer.close()

    def check_auction_end(self, auction_id, prev_end_auction):
        """
        Метод, осующествляющий проверку конца аукциона.
        Если время вышло, то закрывает аукцион, если нет, то ставит новый таймер.
        """

        cur_end_auction = get_auction_bid(auction_id).end_bidding
        if cur_end_auction > prev_end_auction:
            end_auction_timedelta = cur_end_auction - current_datetime()
            tornado.ioloop.IOLoop.current().add_timeout(end_auction_timedelta,
                                                        self.check_auction_end,
                                                        auction_id,
                                                        cur_end_auction)
        else:
            self.auction.finish()
            tornado.ioloop.IOLoop.current().add_timeout(timedelta(seconds=1),
                                                        self.group_send,
                                                        self.auction.id,
                                                        {'auction_is_finished': True})

    def on_close(self):
        self.waiters[self.clients_group_name].remove((self, self.user))
        logging.info('Auction{auction_id}: closed'.format(auction_id=self.auction.id))



