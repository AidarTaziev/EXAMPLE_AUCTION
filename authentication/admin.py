from django.contrib import admin
from . import models as auth_models
from . import forms as auth_forms
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group
from profile import models as profile_models
from django.contrib.auth.models import Permission


class UserAdmin(UserAdmin):
    # inlines = (CompanyMemberInline,)
    form = auth_forms.AdminUserChangeForm
    add_form = auth_forms.AdminSignupForm
    verbose_name_plural = "Регистрация участника"
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Права доступа', {
            'fields': ('is_staff', 'is_superuser'),
        }),
        ('Компания', {
            'fields': ('company',)
        }),
        ('Группы', {
            'fields': ('groups',)
        }),
        ('Уведомления', {
            'fields': ('creating_auction_notification', 'starting_auction_notification', 'cancel_auction_notification')
        }),
    )

    list_display = ('username', 'first_name', 'last_name','company', 'is_staff')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email','first_name','last_name','company','groups', 'password1', 'password2'),
        }),
    )

# admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(Permission)
admin.site.register(auth_models.User, UserAdmin)
