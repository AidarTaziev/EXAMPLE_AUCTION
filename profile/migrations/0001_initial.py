# Generated by Django 2.2.7 on 2019-12-09 14:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import profile.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationBranch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'Отрасль организации',
                'verbose_name_plural': 'Отрасль организации',
            },
        ),
        migrations.CreateModel(
            name='PolymerNotifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polymer_id', models.IntegerField(verbose_name='Id полимера')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Уведомление с полимером',
                'verbose_name_plural': 'Уведомление с полимером',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inn', models.CharField(max_length=12, unique=True, validators=[profile.validators.inn_validator], verbose_name='ИНН')),
                ('full_name', models.CharField(max_length=255, verbose_name='Полное наименование организации')),
                ('short_name', models.CharField(max_length=255, verbose_name='Краткое наименование организации')),
                ('specialization', models.CharField(max_length=255, null=True, verbose_name='Специализация организации')),
                ('phone_number', models.CharField(max_length=255, null=True, verbose_name='Номер телефона')),
                ('fax_number', models.CharField(max_length=255, null=True, verbose_name='Номер факса')),
                ('email', models.EmailField(max_length=254, null=True)),
                ('bank_name', models.CharField(max_length=255, null=True, verbose_name='Банк')),
                ('kpp', models.CharField(max_length=255, null=True, verbose_name='КПП')),
                ('ogrn', models.CharField(max_length=255, null=True, verbose_name='ОГРН')),
                ('okato', models.CharField(max_length=255, null=True, verbose_name='Код ОКАТО')),
                ('bik', models.CharField(max_length=9, null=True, verbose_name='БИК')),
                ('correspondent_account', models.CharField(max_length=255, null=True, verbose_name='Корреспондентский счет')),
                ('sittlement_account', models.CharField(max_length=255, null=True, verbose_name='Расчетный счет')),
                ('legal_address', models.CharField(max_length=255, null=True, verbose_name='Юридический адрес')),
                ('mailing_address', models.CharField(max_length=255, null=True, verbose_name='Почтовый адрес')),
                ('postcode', models.CharField(max_length=255, null=True, verbose_name='Почтовый индекс')),
                ('branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='profile.OrganizationBranch', verbose_name='Отрасль деятельности организации')),
            ],
            options={
                'verbose_name': 'компанию',
                'verbose_name_plural': 'Компания',
            },
        ),
    ]
