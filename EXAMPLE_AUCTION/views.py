import logging
from django.contrib.auth.decorators import permission_required, login_required
from django.views import View
from django.views.generic import TemplateView
from django.db.models import F
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from EXAMPLE_AUCTION.models import Document
from auction.auction_bid_methods import get_auction_bid
from auction.forms import AuctionForm
from auction.auction_bids_list_methods import get_current_auctions_bids_qs, get_my_auctions_qs, polymer_filter_qs
from profile.models import Company
from utils.response_handler.response_object import get_file_page
from utils.sellects.sellect import get_catalogues_data
from utils.decorators.user_decorators import company_required


logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG,
                    filename=u'EXAMPLE_AUCTION.log')


class TradeOffersView(View):
    '''
     Контроллер, возвращающий json ответ со списком заявок, соответсвующих параметрам звапроса.
     :param request:
     :return:
    '''

    def get(self, request, *args, **kwargs):
        show_my_auctions = request.GET['show_my_auctions']
        needed_bids = request.GET['needed_bids']
        polymer_shortcode = request.GET['polymer_shortcode']
        polymer_type = request.GET['polymer_type']
        polymer_plant = request.GET['polymer_plant']

        auction_qs = get_current_auctions_bids_qs(needed_bids)

        if show_my_auctions and request.user.is_authenticated:
            auction_qs = get_my_auctions_qs(auction_qs, request.user)

        if polymer_shortcode or polymer_plant or polymer_type:
            auction_qs = polymer_filter_qs(auction_qs, polymer_shortcode, polymer_type, polymer_plant)

        return JsonResponse({'auctions': [auction.get_display_data() for auction in auction_qs]}, safe=False)


class DocumentsPageView(TemplateView):
    model = Document
    template_name = "EXAMPLE_AUCTION/documents.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['docs'] = self.model.objects.filter(type__name='juristic').order_by('prioritet')
        return context


@method_decorator([login_required], name='dispatch')
class TradeOfferInfoView(View):
    def post(self, request, *args, **kwargs):
        try:
            if request.user.has_perm('EXAMPLE_AUCTION.add_auction'):
                trade_offer_id = int(request.POST.get('trade_offer_id'))
                template_name = request.POST.get('template_name')
                trade_offer = get_auction_bid(trade_offer_id)

            if trade_offer.seller == request.user:
                data = {}

                if template_name:
                    trade_offer.template_name = template_name
                    trade_offer.save(is_updated=True)
                    data['rename_trade_offer'] = True

                data['trade_offer'] = trade_offer.get_display_data()

                return JsonResponse(data, safe=False)
        except Exception as ex:
            logging.error(ex)
            return JsonResponse(status=500)


class CompanyShortInfoView(View):
    """
      Контроллер, возвращающий по ИНН информацию о компании
      :param request:
      :return:
    """

    @method_decorator(permission_required('EXAMPLE_AUCTION.add_auction', raise_exception=True))
    def dispatch(self, request):
        return super(AuctionCreateOfferView, self).dispatch(request)

    def post(self, request, *args, **kwargs):
        inn = request.POST.get('inn')
        if Company.objects.filter(inn=inn).exists():
            company = Company.objects.get(inn=inn)
            return JsonResponse({'company_id': company.id, 'company_short_name': company.short_name}, safe=False)
        else:
            return JsonResponse({'company_exist': False}, safe=False)


class AuctionCreateOfferView(View):
    form_class = AuctionForm
    catalogues_data = get_catalogues_data()
    template_name = 'EXAMPLE_AUCTION/create_trade_offer_page.html'

    @method_decorator(permission_required('EXAMPLE_AUCTION.add_auction', raise_exception=True))
    @method_decorator(company_required)
    def dispatch(self, request):
        return super(AuctionCreateOfferView, self).dispatch(request)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context=self.catalogues_data)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            saved_bidding_offer = form.save()
            if saved_bidding_offer:
                if saved_bidding_offer.save_seller_offer(request.POST):
                    saved_bidding_offer.send_notifications()
                    return HttpResponse('Ваша заявка отправлена')
                else:
                    return HttpResponse('Ошибка валидации полей', status=400)
            else:
                return HttpResponse('Ошибка валидации полей', status=400)
        else:
            logging.error(form.errors)
            return HttpResponse('Ошибка валидации полей', status=400)


#TODO: ПЕРЕДЕЛАТЬ НА CLASS-BASED С МИКСИНОМ
def get_document_page(request, file_name):
    if Document.objects.filter(name=file_name).exists():
        doc = Document.objects.get(name=file_name)
        if doc.type.name == 'juristic': return get_file_page(request, 'media/' + str(doc.path))
    else:
        return HttpResponseNotFound('Ресурс не был найден.')