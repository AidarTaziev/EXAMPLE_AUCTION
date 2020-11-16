import json
import logging
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.httpclient
from datetime import timedelta
from utils.time_customization.custom_time import current_datetime
from auction.auction_bet_methods import check_added_bet_is_increased, format_bet_to_save, save_added_bet
from auction.auction_bid_methods import get_auction_bid, get_auction_seller_offer
from authentication.user_methods import get_user_for_cookie
from auction.bidding_websockets.base_auction import BaseAuctionWebSocket

logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'auction.log')


class HollandAuctionWebSocket(BaseAuctionWebSocket):

    async def open(self, auctionId):
        self.auction = get_auction_bid(auctionId)
        self.session_name = 'auction%d' % self.auction.id
        self.clients_group_name = '%d:clients' % self.auction.id
        self.saller_offer = self.auction.current_seller_offer
        self.user = get_user_for_cookie(self.get_cookie("sessionid"))

        self.check_auction_status()
        self.set_auction_callback()
        self.set_price_refresh_callback()
        self.add_user_to_waiters()
        self.send_session_data_to_user()

    def set_price_refresh_callback(self):
        """
        Метод, отвечающий за установку коллбэка обновления цены (уменьшения цены)
        """

        if self.session_name not in self.auction_refresh_callback:
            refresh_timedelta = (self.auction.end_bidding - current_datetime()).seconds % self.auction.fixation_duration
            loop = tornado.ioloop.IOLoop.current()
            auction_freshcallback = loop.add_timeout(timedelta(seconds=refresh_timedelta) + timedelta(seconds=0.5), self.refresh_session_data_handler)
            self.auction_refresh_callback[self.session_name] = auction_freshcallback

    def refresh_session_data_handler(self):
        """
        Метод, отвечающий за обрабо обновление сессии аукциона
        """

        for waiter in self.waiters[str(self.auction.id) + ':clients']:
            try:
                data = self.auction.get_auction_session_data(self.user)
                waiter[0].write_message(json.dumps(data, ensure_ascii=False, default=str))
            except Exception as ex:
                logging.warning('auction{auction_id}: Send to user exception - {ex}'.format(auction_id=self.auction.id, ex=ex))

        if self.auction.current_seller_offer.middle_price_per_tone != self.auction.current_seller_offer.stop_price_per_tone:
            loop = tornado.ioloop.IOLoop.current()
            loop.add_timeout(timedelta(seconds=self.auction.fixation_duration), self.refresh_session_data_handler)

    async def on_message(self, message):
        if self.auction.status == 'active':
            data_json = json.loads(message)
            self.added_bet_handler(data_json['bet'])
        else:
            self.group_send(self.auction.id, {"type": "send.finished.auction.message"})

    def added_bet_handler(self, added_bet):
        """
        Метод, отвечающий за обработку добавленной ставки
        """

        logging.info('Auction{auction_id}: User {user} added bet - {added_bet} '.
                     format(auction_id=self.auction.id, user=self.user, added_bet=added_bet))

        if self.user != self.auction.seller:
            check_added_bet_is_increased(added_bet)
            added_bet = save_added_bet(format_bet_to_save(added_bet, self.user))

            fixation_bets = self.auction.get_fixation_bets_ids_list()
            if not added_bet:
                self.write_message(
                    json.dumps({'error_message': 'Ставка не прошла валидацию'}, ensure_ascii=False, default=str))
            else:
                if added_bet.id in fixation_bets:
                    if added_bet.is_middle_in_fixation_bets:
                        addedBet_index = fixation_bets.index(added_bet.id)
                        fixation_bets = fixation_bets[addedBet_index + 1:]
                    else:
                        fixation_bets = [added_bet.id, ]

                    self.auction.check_end_to_continue(added_bet)
                    self.auction.set_fixation_time_to_bets(fixation_bets)
                    fix_bet_timedelta = timedelta(seconds=self.auction.fixation_duration)
                else:
                    price_times = (self.auction.current_seller_offer.start_price_per_tone - added_bet.bet_price_per_tone) / self.auction.step
                    fix_bet_timedelta = self.auction.start_bidding + timedelta(seconds=int(price_times * self.auction.fixation_duration)) - current_datetime() + timedelta(seconds=self.auction.fixation_duration)
                    added_bet.set_end_fixation_datetime(self.auction.start_bidding + timedelta(seconds=int(price_times * self.auction.fixation_duration)) + timedelta(seconds=20))

                self.group_send_added_bet(added_bet)
                tornado.ioloop.IOLoop.current().add_timeout(fix_bet_timedelta,
                                                            self.bet_fixation_timeout_callback,
                                                            added_bet)




