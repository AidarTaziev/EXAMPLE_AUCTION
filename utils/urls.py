from django.conf.urls import url
from django.urls import include, path
from . import views
from .feedback import views as views_feedback
from .parsing import views as views_parsing

app_name = 'utils'

urlpatterns = [
    #url(r'^addCompany', views.py.add_company, name='company adding'),
    url(r'^feedback', views_feedback.feedback, name='users feedback'),
    url(r'^news', views_parsing.get_kartli_news, name='kartli.ch news'),
]
