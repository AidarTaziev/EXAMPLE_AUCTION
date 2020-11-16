from django.shortcuts import render
from django.http import HttpResponse, JsonResponse as JSON
from .kartli_ch_news import News

def get_kartli_news(request):
    if request.method == 'GET':
        return createResponseObject(False, News().get_news())
        # try:
        #     news = News().get_news()
        #     return createResponseObject(False, news)
        #
        # except Exception as e:
        #     print(e)
        #     return createResponseObject(True, "Ошибка получения новостей")


def createResponseObject(error, data):
    return JSON({'error': error, 'data': data})
