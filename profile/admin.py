from django.contrib import admin
from . import models
from . import forms
from django.contrib.auth.admin import UserAdmin


class CompanyInline(admin.StackedInline):
    model = models.OrganizationBranch


class CompanyAdmin(admin.ModelAdmin):
    # inlines = (CompanyInline,)
    # exclude = ['user', 'invite_code']
    verbose_name = "Регистрация компании"
    verbose_name_plural = "Регистрация компании"
    # form = forms.Company
    list_display = ('short_name', 'inn')


admin.site.register(models.Company, CompanyAdmin)
admin.site.register(models.OrganizationBranch)
