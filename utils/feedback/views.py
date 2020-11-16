from django.shortcuts import render
from django.http import HttpResponse, JsonResponse as JSON
from . import forms
import threading

def feedback(request):
    form = forms.Question()
    if request.method == 'POST':
        form = forms.Question(data=request.POST)
        if form.is_valid():

            threading.Thread(target=form.send_to_managers).start()

            return createResponseObject(False, 'Ваш вопрос принят на обработку')
        else:
            return createResponseObject(True, form.errors)


def createResponseObject(error, data):
    return JSON({'error': error, 'data': data})
