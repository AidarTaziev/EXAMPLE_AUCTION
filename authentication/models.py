from django.db import models
from django.contrib.auth.models import AbstractUser
from profile import models as profile_models


class User(AbstractUser):
    creating_auction_notification = models.BooleanField(default=False, verbose_name='Уведомлять о создании аукционов')
    starting_auction_notification = models.BooleanField(default=False, verbose_name='Уведомлять о начале аукционов')
    cancel_auction_notification = models.BooleanField(default=False, verbose_name='Уведомлять об отмене аукционов')
    company = models.ForeignKey(profile_models.Company, null=True, on_delete=models.SET_NULL, verbose_name='Компания')

    class Meta:
        verbose_name = "пользователя"
        verbose_name_plural = "Пользователь"

    def get_user_company_data(self):
        company_dict = self.company.__dict__
        for field_name in company_dict:
            if not company_dict[field_name]:
                company_dict[field_name] = ''

        return company_dict
