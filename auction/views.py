import logging
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views import View
from django.views.generic import TemplateView
from auction.models import AuctionDeal
from utils.files_generating.gen_file import generate_bidding_protocol_for_deal
from utils.decorators.user_decorators import company_required
from utils.response_handler.response_object import get_file_page
from .auction_bid_methods import get_auction_bid


logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'EXAMPLE_AUCTION.log')


@method_decorator([login_required, company_required], name='dispatch')
class AuctionSessionPageView(TemplateView):
    template_name = "auction/typical_bidding_session_page.html"

    def get_context_data(self, **kwargs):
        auction_id = kwargs['auction_id']
        auction = get_auction_bid(auction_id)
        if auction.type.name == 'Встречный':
            self.template_name = "auction/counter_bidding_session_page.html"
        elif auction.type.name == 'Голландский':
            self.template_name = "auction/holland_bidding_session_page.html"
        else:
            self.template_name = "auction/typical_bidding_session_page.html"

        context = auction.get_display_data()
        return context


@method_decorator([login_required, company_required], name='dispatch')
class AuctionPropertiesPageView(TemplateView):
    template_name = "auction/propertys_page.html"

    def get_context_data(self, **kwargs):
        auction_id = kwargs['auction_id']
        auction = get_auction_bid(auction_id)

        context = auction.get_display_data()
        if self.request.user == auction.seller or self.request.user.has_perm('authentication.can_view_all_data'):
            context['deals'] = [deal.get_display_data(self.request.user) for deal in auction.get_all_deals()]
            context['all_bets'] = [bet.get_display_data(self.request.user) for bet in auction.get_all_bets()]
        else:
            context['deals'] = [deal.get_display_data(self.request.user) for deal in auction.get_client_deals(self.request.user)]
            context['all_bets'] = [bet.get_display_data(self.request.user) for bet in auction.get_all_bets()]

        context['auction_status'] = auction.status

        return context


#TODO: ПЕРЕДЕЛАТЬ НА CLASS-BASED С МИКСИНОМ
@login_required(login_url='/need_auth_error')
def auction_protocol_for_deal(request, auction_id, deal_id):
    """
    Контроллер, отвечающий за генерацию/возврат протокола торгов
    :param request:
    :param auction_id:
    :param deal_id:
    :return:
    """

    try:
        auction = get_auction_bid(auction_id)
        deal = AuctionDeal.objects.get(id=deal_id)

        if request.user == deal.bet.client\
                or request.user == auction.seller \
                or request.user.has_perm('authentication.can_view_all_data'):

            out_put_full_path = generate_bidding_protocol_for_deal(deal)
            return get_file_page(request, out_put_full_path)
        else:
            return HttpResponse(status=403)
    except:
        return HttpResponseNotFound('<h1>Данного файла не существует!</h1>')


#TODO: СМЕНИТЬ УСЛОВИЕ НА ДЕКОРАТОР ПРОВЕРКИ НА ПОЛЬЗОВАТЕЛЯ ПРОДАВЦА
@method_decorator([login_required], name='dispatch')
class CancelAuctionView(View):
    def post(self, request, *args, **kwargs):
        auction_id = int(request.POST['auction_id'])
        auction = get_auction_bid(auction_id)
        if auction.seller == request.user:
            if auction.have_bets:
                return JsonResponse({'auction_cancel': False,
                                     'message': 'Вы не можете отменить аукцион, потому что аукцион идет'})
            else:
                auction.delete()
                return JsonResponse({'auction_cancel': True, 'message': 'Аукцион успешно отменен'})
        else:
            return JsonResponse(status=403)


