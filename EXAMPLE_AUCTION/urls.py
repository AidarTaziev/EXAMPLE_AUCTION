from django.conf.urls import url
from django.contrib import admin
from django.urls import include
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf import settings
from EXAMPLE_AUCTION import views
from EXAMPLE_AUCTION.views import AuctionCreateOfferView, DocumentsPageView, TradeOffersView, TradeOfferInfoView, \
    CompanyShortInfoView
from auction import views as auction_views
from sprav.requests import get_all_plants_types


urlpatterns = [url(r'^admin_panel/', admin.site.urls),
               url(r'^bank_account/', include('bank_account.urls')),
               url(r'^auction/', include('auction.urls')),
               url(r'^auth/', include('authentication.urls')),
               url(r'^profile/', include('profile.urls')),
               url(r'^utils/', include('utils.urls')),

               url(r'^get_trade_offers', TradeOffersView.as_view()),
               url(r'^get_trade_offer_info', TradeOfferInfoView.as_view()),
               url(r'^check_company', CompanyShortInfoView.as_view()),
               url(r'^create_trade_offer', AuctionCreateOfferView.as_view(), name="create_trade_offer"),
               url(r'^documents/', DocumentsPageView.as_view(), name='documents'),

               url(r'^document/(?P<file_name>([^\\]+))', views.get_document_page),
               url(r'^protocol/auction(?P<auction_id>\d+)/deal(?P<deal_id>\d+)/',
                   auction_views.auction_protocol_for_deal),

               url(r'^incoterms/', TemplateView.as_view(template_name="EXAMPLE_AUCTION/incoterms.html"),
                   name='incoterms'),
               url(r'^no_company_error', TemplateView.as_view(template_name="errors/no_company_error.html")),
               url(r'^need_auth_error', TemplateView.as_view(template_name="errors/need_auth_error.html")),
               url(r'^no_found_error', TemplateView.as_view(template_name="errors/404_error.html")),
               url(r'^server_error', TemplateView.as_view(template_name="errors/505_error.html")),
               url('', TemplateView.as_view(template_name="EXAMPLE_AUCTION/trade_offers_list_page.html",
                                            extra_context=get_all_plants_types()), name="trade_offers"),
               ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
