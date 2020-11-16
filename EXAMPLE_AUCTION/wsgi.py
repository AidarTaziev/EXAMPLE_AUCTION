

# +++++++++++ DJANGO +++++++++++
# To use your own Django app use code like this:
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EXAMPLE_AUCTION.settings')

application = get_wsgi_application()

