from django.db import models
from django.core.validators import FileExtensionValidator


class TradingType(models.Model):
    name = models.CharField(unique=True, max_length=100)


class TradingOperation(models.Model):
    name = models.CharField(unique=True, max_length=100)


class BidLevel(models.Model):
    name = models.CharField(unique=True, max_length=100)


class ShipmentConditions(models.Model):
    name = models.CharField("Условия доставки", unique=True, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Условия доставки"
        verbose_name_plural = "Условия доставки"


class ShipmentMethods(models.Model):
    name = models.CharField("Метод доставки", unique=True, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Метод доставки"
        verbose_name_plural = "Методы доставки"


class PaymentTerms(models.Model):
    name = models.CharField(unique=True, max_length=100, verbose_name='Наименование способа платежа')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Способ платежа"
        verbose_name_plural = "Способы платежей"


class ParticipationStatus(models.Model):
    name = models.CharField(unique=True, max_length=100, verbose_name='Название статуса участия')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус участия"
        verbose_name_plural = "Статусы участия"


class DocumentType(models.Model):
    name = models.CharField(unique=True, max_length=100, verbose_name='Тип документа')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип документа"
        verbose_name_plural = "Тип документов"


class Document(models.Model):
    type = models.ForeignKey(DocumentType, models.DO_NOTHING, verbose_name="Тип документа")
    name = models.CharField(max_length=200, verbose_name='Название документа')
    path = models.FileField(upload_to='documents/', blank=True, verbose_name="Документ", validators=[FileExtensionValidator(['pdf'])])
    prioritet = models.IntegerField(null=True, blank=True)
    last_modified = models.DateTimeField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"



