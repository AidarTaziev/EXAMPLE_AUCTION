import json
import copy
import logging
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.httpclient
from datetime import timedelta
from auction.auction_bet_methods import check_added_bet_is_increased, format_bet_to_save, save_added_bet
from auction.bidding_websockets.base_auction import BaseAuctionWebSocket


logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'auction.log')


class TypicalAuctionWebSocket(BaseAuctionWebSocket):
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

        logging.info('auction{auction_id}: User {user} added bet - {added_bet} '.
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
                    logging.info('auction{auction_id}: added bet fixation bets {fixation_bets} '.
                                 format(auction_id=self.auction.id, fixation_bets=fixation_bets))

                    if added_bet.id == fixation_bets[0]:
                        fixation_bets = fixation_bets
                    elif added_bet.is_middle_in_fixation_bets:
                        addedBet_index = fixation_bets.index(added_bet.id)
                        fixation_bets = fixation_bets[addedBet_index:]
                    else:
                        fixation_bets = [added_bet.id, ]

                    self.auction.check_end_to_continue(added_bet)
                    self.auction.set_fixation_time_to_bets(fixation_bets)

                self.group_send_added_bet(added_bet)
                tornado.ioloop.IOLoop.current().add_timeout(timedelta(seconds=self.auction.fixation_duration),
                                                            self.bet_fixation_timeout_callback,
                                                            added_bet)

