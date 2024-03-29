# Generated by Django 2.2.7 on 2019-12-09 14:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BidLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Тип документа')),
            ],
            options={
                'verbose_name': 'Тип документа',
                'verbose_name_plural': 'Тип документов',
            },
        ),
        migrations.CreateModel(
            name='ParticipationStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название статуса участия')),
            ],
            options={
                'verbose_name': 'Статус участия',
                'verbose_name_plural': 'Статусы участия',
            },
        ),
        migrations.CreateModel(
            name='PaymentTerms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Наименование способа платежа')),
            ],
            options={
                'verbose_name': 'Способ платежа',
                'verbose_name_plural': 'Способы платежей',
            },
        ),
        migrations.CreateModel(
            name='ShipmentConditions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Условия доставки')),
            ],
            options={
                'verbose_name': 'Условия доставки',
                'verbose_name_plural': 'Условия доставки',
            },
        ),
        migrations.CreateModel(
            name='ShipmentMethods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Метод доставки')),
            ],
            options={
                'verbose_name': 'Метод доставки',
                'verbose_name_plural': 'Методы доставки',
            },
        ),
        migrations.CreateModel(
            name='TradingOperation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TradingType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название документа')),
                ('path', models.FileField(blank=True, upload_to='documents/', validators=[django.core.validators.FileExtensionValidator(['pdf'])], verbose_name='Документ')),
                ('prioritet', models.IntegerField(blank=True, null=True)),
                ('last_modified', models.DateTimeField(blank=True)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='EXAMPLE_AUCTION.DocumentType', verbose_name='Тип документа')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
            },
        ),
    ]
