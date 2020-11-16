from django.conf.urls import url
from django.urls import include, path
from . import views

app_name = 'profile'

urlpatterns = [
    # url(r'^auth/', include('django.contrib.auth.urls')),
    # path('login_page/', views.py.login_page, name = 'login_page'),
    # url(r'^auctions', views.py.get_auctions, name='user auctions'),
    # url(r'^winbets', views.py.get_win_bets, name='user winning bets'),
    # url(r'^addCompany', views.py.add_company, name='company adding'),
    url(r'^update', views.update_profile, name='profile updating'),
    # url(  r'^join', views.py.company_invite_code_join, name='company join'),
    url(r'^filter', views.history_search, name='EXAMPLE_AUCTION history filter'),
    # url(r'^reqs_update', views.py.update_requisites, name='update requisites'),
    url('^(?P<user_id>\d+)', views.page_profile, name='page_profile'),
    url('^company/(?P<company_id>\d+)', views.page_company, name='page_profile'),
    url('^notifications/types', views.notifications_params, name='notifications_params'),
    url('', views.personal_page, name='page_profile'),
    #url('addcompany', views.py.addcompany, name='')
]
