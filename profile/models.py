from django.db import models
from django.conf import settings
from profile.validators import *


class OrganizationBranch(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Отрасль организации"
        verbose_name_plural = "Отрасль организации"


class Company(models.Model):
    inn = models.CharField(unique=True, max_length=12, verbose_name="ИНН", validators=[inn_validator])
    full_name = models.CharField(max_length=255, null=False, verbose_name="Полное наименование организации")
    short_name = models.CharField(max_length=255, null=False, verbose_name="Краткое наименование организации")
    branch = models.ForeignKey(OrganizationBranch, null=True, on_delete=models.DO_NOTHING, verbose_name="Отрасль деятельности организации")
    specialization = models.CharField(max_length=255, null=True, verbose_name="Специализация организации")
    phone_number = models.CharField(max_length=255, null=True, verbose_name="Номер телефона")
    fax_number = models.CharField(max_length=255, null=True, verbose_name="Номер факса")
    email = models.EmailField(null=True,)
    bank_name = models.CharField(null=True, max_length=255, verbose_name="Банк")
    kpp = models.CharField(unique=False, null=True, verbose_name="КПП", max_length=255)
    ogrn = models.CharField(unique=False, null=True, verbose_name="ОГРН", max_length=255)
    okato = models.CharField(unique=False, null=True, verbose_name="Код ОКАТО", max_length=255)
    bik = models.CharField(unique=False, null=True, verbose_name="БИК", max_length=9)
    correspondent_account = models.CharField(unique=False, null=True, verbose_name="Корреспондентский счет", max_length=255)
    sittlement_account = models.CharField(unique=False, null=True, verbose_name="Расчетный счет", max_length=255)
    legal_address = models.CharField(max_length=255, null=True, verbose_name="Юридический адрес")
    mailing_address = models.CharField(max_length=255, null=True, verbose_name="Почтовый адрес")
    postcode = models.CharField(verbose_name="Почтовый индекс", null=True, max_length=255)
    # invite_code = models.CharField(max_length=8, verbose_name="Код приглашения")

    def __str__(self):
        return self.short_name + " " + self.inn

    class Meta:
        verbose_name = "компанию"
        verbose_name_plural = "Компания"


class PolymerNotifications(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    polymer_id = models.IntegerField(verbose_name="Id полимера")

    class Meta:
        verbose_name = "Уведомление с полимером"
        verbose_name_plural = "Уведомление с полимером"

    def __str__(self):
        return "{0} {1}".format(self.client.last_name, self.client.first_name)
