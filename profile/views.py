from django.shortcuts import render, redirect
from auction import models as auction_models
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from . import forms, models
import random
import datetime
import  json
from django.db.models import Max, Min
from sprav.requests import get_types_ref_polymers
from authentication import models as auth_models
from utils.response_handler.response_object import create_response_object
from .profile_methods.bidding_statistics import auction_info
from .profile_methods.bidding_history import deals_date_separation
from auction.auction_bid_methods import user_auctions_qs
from profile.profile_methods.polymer_type_list import get_user_polymers_list
from profile.profile_methods.notification_params_validation import polymer_notification_validation

"""
Фильтр сделок в истории
"""
@login_required
def history_search(request):
    if request.method == 'POST':

        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        auctions = date_filter_auctions(request.user, start_date, end_date)
        if len(auctions) > 0:
            return create_response_object(False, auctions)
        else:
            return create_response_object(False, [])


# @permission_required(('EXAMPLE_AUCTION.add_auctionbid', 'EXAMPLE_AUCTION.can_view_all_bidding_session'))
def page_company(request, company_id=None):
    # TODO: ЗАМЕНИТЬ PERMISSIONS НА ОСНОВЕ ДЕКОРАТОРОВ
    if request.method == 'GET':
        if request.user.has_perm('authentication.can_view_all_data') or\
            request.user.has_perm('EXAMPLE_AUCTION.add_auction') or\
            str(request.user.company.id) == company_id:

            company_arr = models.Company.objects.filter(id=company_id)
            if not company_arr:
                return HttpResponse('<h4>Такой компании нет!</h4>')
            context = {
                'company': company_arr[0],
                'statistic': auction_info(auth_models.User.objects.filter(company=company_arr[0]))
            }

            return render(request, 'profile_view/company.html', context)

        else:
            return redirect('/')


def page_profile(request, user_id=None):
    #TODO: ЗАМЕНИТЬ PERMISSIONS НА ОСНОВЕ ДЕКОРАТОРОВ
    if request.user.has_perm('authentication.can_view_all_data') or \
        request.user.has_perm('EXAMPLE_AUCTION.add_auction') or \
        str(request.user.id) == user_id:
        if request.method == 'GET':
            if user_id is None:
                return redirect('/profile/')

            user_qs = auth_models.User.objects.filter(id=user_id)

            if user_qs.exists():
                user = user_qs[0]

                context = {
                    'company': user.company,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'last_login': user.last_login,
                    'statistic': auction_info([user]),
                }
                return render(request, 'profile_view/profile.html', context)
            else:
                # context = {
                #     'error': True,
                #     'message': 'Пользователя не существует!'
                # }
                # return render(request, 'profile_view/profile.html', context)
                return HttpResponse('<h4>Такого пользователя нет!</h4>')
    else:
        return redirect('/')


@login_required
def personal_page(request):
     if request.method == 'GET':
         branches = models.OrganizationBranch.objects.all()

         context = {
             'creating_auction_notification': request.user.creating_auction_notification,
             'starting_auction_notification': request.user.starting_auction_notification,
             'cancel_auction_notification': request.user.cancel_auction_notification,
             'biddings': deals_date_separation(request.user),
             'companies_branches': branches,
             'user_company': request.user.company,
             'is_seller': is_seller(request.user),
             'polymer_types': get_user_polymers_list(request.user),
         }
         return render(request, 'profile/profile.html', context=context)


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = forms.Profile(data=request.POST, request=request)
        if form.is_valid():
            form.update()
            return create_response_object(False, 'OK')
        else:
            return create_response_object(True, form.errors)


def date_filter_auctions(user, start_date_req=None, end_date_req=None):

    user_auctions = user_auctions_qs(user)
    blocks_to_hide = []
    try:
        start_date = datetime.datetime.strptime(start_date_req, '%Y-%m-%d').date()
    except:
        start_date = auction_models.Auction.objects.aggregate(Min('start_bidding'))['start_bidding__min'].date()

    try:
        end_date = datetime.datetime.strptime(end_date_req, '%Y-%m-%d').date()
    except:
        end_date = auction_models.Auction.objects.aggregate(Max('start_bidding'))['start_bidding__max'].date()

    date_separation = user_auctions.dates('start_bidding', 'day').reverse()
    block_counter = 0
    for date in date_separation:
        if date < start_date:
            blocks_to_hide.append(block_counter)
        elif date > end_date:
            blocks_to_hide.append(block_counter)
        block_counter += 1

    return blocks_to_hide


def is_seller(user):
    return user.has_perm('EXAMPLE_AUCTION.add_auction')


@login_required
def notifications_params(request):
    if request.method == 'POST':

        print(request.POST)
        polymers = json.loads(request.POST.getlist('polymers')[0])

        error = polymer_notification_validation(polymers, request.user)

        if error:
            return create_response_object(True, error)
        else:
            return create_response_object(False, 'Параметры уведомлений успешно обновлены')
