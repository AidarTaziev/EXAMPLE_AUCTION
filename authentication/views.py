from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login as login_auth
from django.http import HttpResponseRedirect
from authentication.auth_methods import auth_logout
from . import forms
from utils.response_handler.response_object import create_response_object


def login(request):
    """
    Метод аутентификации с полями username и password
    :param request: Объект запроса django, хранит в себе headers, data
    :return: http ответ с результатом аутентификации
    """
    if request.method == 'POST':
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            login_auth(request, form.user)
            return create_response_object(False, 'Успешно')
        else:
            return create_response_object(True, error_handler(form.errors))


def acc_logout(request):
    """
    Метод выхода аккаунта из профиля, очищает сессию
    :param request: Объект запроса django, хранит в себе headers, data
    :return: переадресацию на главную страницу
    """
    if settings.LOCAL_SETTINGS:
        logout(request)
        return redirect('/')
    else:
        return auth_logout(request)


def login_page(request):
    """
    Метод отрисовки html страницы
    :param request: Объект запроса django, хранит в себе headers, data
    :return: переадресацию на главную страницу
    """
    if not request.user.is_authenticated:
        if settings.LOCAL_SETTINGS:
            return render(request, 'auction_sign/sign.html')
        else:
            login_url = '{passport_domain}/auth/?next={base_uri}'\
                        .format(passport_domain=settings.PASSPORT_DOMAIN, base_uri=settings.BASE_URI)
            return HttpResponseRedirect(login_url)
    else:
        return redirect('/')


def signup(request):
    if request.method == 'POST':
        form = forms.SignupForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login_auth(request, user)
                return create_response_object(False, 'OK')
            else:
                return create_response_object(True, 'Ошибка авторизации зарегистрированного пользователя')
        else:
            return create_response_object(True, form.errors)


def error_handler(form_errors):
    errors = {}
    for key in form_errors:
        errors[key] = form_errors[key][0]
    return errors
