import tornado.ioloop
from auction.bidding_websockets.counter_auction import CounterAuctionWebSocket
from auction.bidding_websockets.typical_auction import TypicalAuctionWebSocket
from auction.bidding_websockets.holland_auction import HollandAuctionWebSocket

application = tornado.web.Application([
    (r"/ws/typical/auction/bidding_session/([0-9]+)/", TypicalAuctionWebSocket),
    (r"/ws/counter/auction/bidding_session/([0-9]+)/", CounterAuctionWebSocket),
    (r"/ws/holland/auction/bidding_session/([0-9]+)/", HollandAuctionWebSocket),
])