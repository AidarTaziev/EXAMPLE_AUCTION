from django import forms
from django.core.mail import send_mail


class Question(forms.Form):

    email_errors = {
        'required': "Введите вашу почту",
        'invalid': "Введите корректную почту"
    }

    question_errors = {
        'required': "Введите Ваш вопрос",
    }

    email = forms.EmailField(label='Почта', error_messages=email_errors)
    question = forms.CharField(label='Вопрос', error_messages=question_errors)

    def __init__(self, request=None, *args, **kwargs):
        """
        Кастомизация формы
        """
        self.request = request
        # self.user = request.user
        super().__init__(*args, **kwargs)

    def clean(self):
        self.question = self.cleaned_data.get('question')
        self.email = self.cleaned_data.get('email')

    def send_to_managers(self, emails=['bloq@yandex.ru']):

        send_mail(
            'КАРТЛИ. Воспрос пользователя:',
            self.question + ' Задал вопрос: ' + self.email,
            'tazievaidar1998@gmail.com',
            [emails],
            fail_silently=False,
        )
