import os
import signal
import time
import ssl
import tornado.httpserver
import tornado.ioloop
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from auction.bidding_websockets.config import application


class Command(BaseCommand):
    args = '[port_number]'
    help = 'Starts the Tornado application for message handling.'

    def sig_handler(self, sig, frame):
        tornado.ioloop.IOLoop.instance().add_callback(self.shutdown)

    def shutdown(self):
        self.http_server.stop()

        io_loop = tornado.ioloop.IOLoop.instance()
        io_loop.add_timeout(time.time() + 2, io_loop.stop)

    def handle(self, *args, **options):
        if len(args) == 1:
            try:
                port = int(args[0])
            except ValueError:
                raise CommandError('Invalid port number specified')
        else:
            port = settings.TORNADO_PORT

        if not settings.LOCAL_SETTINGS:
            ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_ctx.load_cert_chain(*settings.HTTPS_CERTS)

            self.http_server = tornado.httpserver.HTTPServer(application, ssl_options=ssl_ctx)
        else:
            self.http_server = tornado.httpserver.HTTPServer(application)

        self.http_server.listen(port, address=settings.TORNADO_HOST)

        signal.signal(signal.SIGTERM, self.sig_handler)
        signal.signal(signal.SIGINT, self.sig_handler)

        loop = tornado.ioloop.IOLoop.current()
        loop.start()