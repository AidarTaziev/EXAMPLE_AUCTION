from django.conf.urls import url
from django.urls import include, path
from authentication import views

app_name = 'authentication'

urlpatterns = [
    # url(r'^auth/', include('django.contrib.auth.urls')),
    # path('login_page/', views.py.login_page, name = 'login_page'),
    url(r'^login$', views.login, name='login'),
    url(r'^signup$', views.signup, name='singup'),
    url(r'^logout$', views.acc_logout, name='logout'),
    url('', views.login_page, name='main')
]
