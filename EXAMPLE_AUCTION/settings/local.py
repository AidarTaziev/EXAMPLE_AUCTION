import os

SECRET_KEY = os.environ['SECRET_KEY']

LOCAL_SETTINGS = True

DEBUG = True

ALLOWED_HOSTS = []

TORNADO_HOST = '127.0.0.1'
TORNADO_PORT = 8888

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'CONN_MAX_AGE': 30536000,
        'NAME': 'EXAMPLE_AUCTION',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'authentication.middleware.SyncUsersMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'utils.middlewares.no_cache.ClearCacheMiddleware',
]

#SESSION
SESSION_COOKIE_NAME = "sessionid"

#PASSPORT
MAIN_DOMAIN = 'unlogic.ru'
PASSPORT_SECRET_KEY = "{0}passport".format(SECRET_KEY)
PASSPORT_DOMAIN = 'https://passport.{0}'.format(MAIN_DOMAIN)
PASSPORT_USER_CREDENTIALS_URI = PASSPORT_DOMAIN + '/auth/data'
PASSPORT_SESSION_ID_NAME = "passport_session_id"

#
SBERBANK_SBBOL_URL = "https://edupir.testsbi.sberbank.ru:9443"
