from django.contrib.auth import logout
from django.shortcuts import HttpResponseRedirect
from django.conf import settings


def auth_logout(request):
    logout(request)
    response = HttpResponseRedirect('/')
    response.delete_cookie(settings.PASSPORT_SESSION_ID_NAME, domain=".{0}".format(settings.MAIN_DOMAIN))
    return response
