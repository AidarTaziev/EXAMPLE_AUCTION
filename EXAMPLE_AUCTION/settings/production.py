import os

SECRET_KEY = os.environ['SECRET_KEY']

BASE_URI = 'https://example.tyu'

TORNADO_HOST = '127.0.0.1'
TORNADO_PORT = 8888

LOCAL_SETTINGS = False

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['example.tyu']

HTTPS_CERTS = ("/etc/letsencrypt/live/example.tyu/fullchain.pem",
               "/etc/letsencrypt/live/example.tyu/privkey.pem")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'CONN_MAX_AGE': 30536000,
        'NAME': 'EXAMPLE_AUCTION',
        'USER': 'root',
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': 'db',
    }
}


#PASSPORT
MAIN_DOMAIN = 'example.tyu'
PASSPORT_URL = "https://passport.example.tyu"
PASSPORT_SECRET_KEY = "{0}passport".format(SECRET_KEY)
PASSPORT_DOMAIN = 'https://passport.{0}'.format(MAIN_DOMAIN)
PASSPORT_USER_CREDENTIALS_URI = 'https://passport.example.tyu' + '/auth/data'
PASSPORT_SESSION_ID_NAME = "passport_session_id"


#SPRAV
POLYMER_SPRAV_SECRET_KEY = os.environ['POLYMER_SPRAV_SECRET_KEY']
POLYMER_SPRAV_FULL_URI = 'https://reference.example.tyu'


# REDIS related settings
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
AUCTION_NOTIFICATION_BD_NAME = "auction_notifications"

#SBER FINTECH
CREDIT_REDIRECT_URN = "/bank_account/credit_redirect"
UNLINK_REDIRECT_URN = "/bank_account/unlink_redirect"