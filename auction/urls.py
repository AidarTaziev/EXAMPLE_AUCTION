from django.conf.urls import url
from . import views
from .views import AuctionPropertiesPageView, AuctionSessionPageView, CancelAuctionView

urlpatterns = [
    url('^properties/(?P<auction_id>\d+)', AuctionPropertiesPageView.as_view(), name="auction_propertys"),
    url('^bidding_session/(?P<auction_id>\d+)', AuctionSessionPageView.as_view(), name="auction_bidding_session"),
    url('^cancel', CancelAuctionView.as_view()),
    # url('^accept_participation_application', views.accept_participation_application),
    # url('^participation_orders', views.get_participation_orders),
]
