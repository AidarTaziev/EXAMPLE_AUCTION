import json
import copy
import logging
import time
# import aioredis
# from aredis import StrictRedis
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.httpclient
from threading import Thread
from datetime import timedelta
from utils.time_customization.custom_time import current_datetime
from auction.auction_bet_methods import check_added_bet_is_increased, format_bet_to_save, save_added_bet
from auction.auction_bid_methods import get_auction_bid, get_auction_seller_offer, format_seller_offer_to_save, save_seller_offer
from authentication.user_methods import get_user_for_cookie
from auction.auction_bet_methods import get_auction_bet
from auction.bidding_websockets.base_auction import BaseAuctionWebSocket

logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'auction.log')


class CounterAuctionWebSocket(BaseAuctionWebSocket):

    async def on_message(self, message):
        if self.auction.status == 'active':
            data_json = json.loads(message)
            if 'seller_offer' in data_json:
                self.added_saller_offer_handler(data_json['seller_offer'])
            elif 'bet' in data_json:
                self.added_bet_handler(data_json['bet'])
            elif 'deleted_bet' in data_json:
                deleted_bet_id = int(data_json['deleted_bet'])
                self.deleted_bet_handler(deleted_bet_id)
            elif 'auction_need_to_finish' in data_json:
                self.auction_needed_to_finish_handler()
        else:
            self.group_send(self.auction.id, {"type": "send.finished.auction.message"})

    def added_saller_offer_handler(self, added_saller_offer):
        """
        Метод, обработчик выставленного продавцом предложения (цена и количество)
        """

        logging.info('Auction{auction_id}: User {user} added offer {added_saller_offer}'.
                     format(auction_id=self.auction.id, user=self.user, added_saller_offer=added_saller_offer))

        if self.user == self.auction.seller:
            fixation_bets = self.auction.get_fixation_bets_ids_list()
            if not fixation_bets:
                # Если нет сделок в области фиксации, то сохраняем выставленное продавцом предложение
                saller_offer = save_seller_offer(format_seller_offer_to_save(added_saller_offer))
                if saller_offer:
                    self.saller_offer = saller_offer
                    # Устанавливаем время фиксации ставок
                    self.auction.set_fixation_time_to_bets(fixation_bets)
                    # Отправляем всем пользователям обновленную информацию о сессии аукциона
                    self.group_send_auction_session_data(fixation_bets)
                    # Устанвавливаем коллюэк на фиксацию сдлки
                    self.set_bet_fixation_callback()

    def set_bet_fixation_callback(self):
        """
        Метод, устанавливающий коллбэк на время фиксации ставки
        """

        data = self.auction.get_auction_session_data(self.user)
        if data['all_bets']:
            added_bet_dict = data['all_bets'][0]
            added_bet = get_auction_bet(added_bet_dict['id'])
            tornado.ioloop.IOLoop.current().add_timeout(timedelta(seconds=self.auction.fixation_duration),
                                                        self.bet_fixation_timeout_callback, added_bet)

    def added_bet_handler(self, added_bet):
        """
        Метод, отвечающий за обработку добавленной ставки
        """

        logging.info('Auction{auction_id}: User {user} added bet - {added_bet} '.
                     format(auction_id=self.auction.id, user=self.user, added_bet=added_bet))

        if self.user != self.auction.seller:
            check_added_bet_is_increased(added_bet)
            added_bet = save_added_bet(format_bet_to_save(added_bet, self.user))

            if not added_bet:
                self.write_message(
                    json.dumps({'error_message': 'Ставка не прошла валидацию'}, ensure_ascii=False, default=str))
            else:
                if self.auction.current_seller_offer:
                    fixation_bets = self.auction.get_fixation_bets_ids_list()
                    if added_bet.id in fixation_bets:
                        if added_bet.is_middle_in_fixation_bets:
                            added_bet_index = fixation_bets.index(added_bet.id)
                            fixation_bets = fixation_bets[added_bet_index + 1:]
                        else:
                            fixation_bets = [added_bet.id, ]

                        self.auction.check_end_to_continue(added_bet)
                        self.auction.set_fixation_time_to_bets(fixation_bets)
                    tornado.ioloop.IOLoop.current().add_timeout(timedelta(seconds=self.auction.fixation_duration),
                                                                self.bet_fixation_timeout_callback,
                                                                added_bet)
                self.group_send_added_bet(added_bet)

    def deleted_bet_handler(self, deleted_bet_id):
        """
        Метод, отвечающий за обработку удаленной ставки
        """

        bet = get_auction_bet(deleted_bet_id)
        if self.user == bet.client:
            if self.auction.current_seller_offer:
                fixation_bets = self.auction.get_fixation_bets_ids_list()
                if deleted_bet_id in fixation_bets:
                    self.write_message({'bet_cannot_deleted': True})
                else:
                    bet.set_is_deleted_bet()
                    self.group_send(self.auction.id, json.dumps({'deleted_bet': bet.id}, ensure_ascii=False, default=str))
            else:
                bet.set_is_deleted_bet()
                self.group_send(self.auction.id, json.dumps({'deleted_bet': bet.id}, ensure_ascii=False, default=str))

    def auction_needed_to_finish_handler(self):
        """
        Метод, осуществляющий закрытие аукциона в случае если заявку на закрытие сделал продавец аукциона,
        и если нет ставок в области фиксации
        """

        if self.user == self.auction.seller:
            fixation_bets = self.auction.get_fixation_bets_ids_list()
            if not fixation_bets:
                self.auction.current_seller_offer.close()
                self.auction.finish()
                tornado.ioloop.IOLoop.current().add_timeout(timedelta(seconds=1),
                                                            self.group_send,
                                                            self.auction.id,
                                                            {'auction_is_finished': True})




