import os

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = True

ALLOWED_HOSTS = ['example.tyu']

HTTPS_CERTS = ("/etc/letsencrypt/live/example.tyu/fullchain.pem",
               "/etc/letsencrypt/live/example.tyu/privkey.pem")


LOCAL_SETTINGS = False

TORNADO_HOST = '127.0.0.1'
TORNADO_PORT = 8889

BASE_URI = 'https://example.tyu'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'CONN_MAX_AGE': 30536000,
        'NAME': 'files_kartli_marketplace',
        'USER': 'root',
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': 'db',
    }
}


#PASSPORT
LOGIN_URL = 'https://passport.unlogic.ru/auth/?next=https://example.tyu/'
MAIN_DOMAIN = 'unlogic.ru'
PASSPORT_URL = "https://passport.unlogic.ru"
PASSPORT_SECRET_KEY = "{0}passport".format(SECRET_KEY)
PASSPORT_DOMAIN = 'https://passport.{0}'.format(MAIN_DOMAIN)
PASSPORT_USER_CREDENTIALS_URI = PASSPORT_DOMAIN + '/auth/data'
PASSPORT_SESSION_ID_NAME = "passport_session_id"
AUCTION_NOTIFICATION_BD_NAME = "auction_notifications_test"


#SBER FINTECH
CREDIT_REDIRECT_URN = "/bank_account/credit_redirect"
UNLINK_REDIRECT_URN = "/bank_account/unlink_redirect"




