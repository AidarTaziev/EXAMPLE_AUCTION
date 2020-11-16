import logging
import redis
from django.template.loader import get_template
from django.contrib.auth import get_user_model
from django.conf import settings
from utils.notifications.send_file import group_send_html_on_emails
from utils.time_customization.custom_time import current_datetime
from auction.models import Auction
from authentication.user_methods import user_followed_on_auctions
from EXAMPLE_AUCTION.celery import app


logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'EXAMPLE_AUCTION.log')

r = redis.Redis()
User = get_user_model()

#TODO: подключение к редису вставить во внутрь задачи-функции
@app.task
def send_start_auction_notifications():
    """
    Функция, осуществляющая отправку уведомлений о начале аукциона. Каждому пользователю отправляется список аукционов
    на которые он подписан.
    """

    try:
        auction_notifications_set = r.smembers(settings.AUCTION_NOTIFICATION_BD_NAME)
        if auction_notifications_set:
            auction_notifications_list = [int(notify.decode('utf8')) for notify in auction_notifications_set]
            for user in User.objects.filter(creating_auction_notification=True):
                user_auction_ids = user_followed_on_auctions(user, auction_notifications_list)
                auctions_data = [auction.get_display_data() for auction in
                                 Auction.objects.filter(id__in=user_auction_ids).order_by('id')]
                if auctions_data:
                    html_content = get_template('email_messages/create_auction_message.html')\
                                                    .render({'auctions_data': auctions_data})
                    group_send_html_on_emails('Информация о торгах ' + current_datetime().strftime('%d.%m.%y'),
                                              '',
                                              html_content,
                                              [user.email])
    except Exception as ex:
        logging.warning("Celery: exception - {ex}".format(ex=ex))
    finally:
        r.delete(settings.AUCTION_NOTIFICATION_BD_NAME)


