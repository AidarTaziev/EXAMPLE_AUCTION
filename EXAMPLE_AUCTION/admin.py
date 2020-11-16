from django.contrib import admin
from EXAMPLE_AUCTION.models import *
from EXAMPLE_AUCTION.forms import *
#
# class MyAdminSite(admin.AdminSite):
#     pass
#     def get_app_list(self, request):
#         """
#         Return a sorted list of all the installed apps that have been
#         registered in this site.
#         """
#
#         app_dict = self._build_app_dict(request)
#         # custom_app_dict =
#         # Sort the apps alphabetically.
#         app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
#
#
#         # Sort the models alphabetically within each app.
#         for app in app_list:
#             app['models'].sort(key=lambda x: x['name'])
#         print(app_list, '\n')
#
#         return app_list
#
# admin.site = MyAdminSite()
#
# class AuctionBidChangeFormAdmin(admin.ModelAdmin):
#     fields = ('polymer', 'shipment_condition', 'shipment_method', 'delivery', 'storage_location',
#               'lot_size', 'payment_term', 'step', 'start_bidding', 'end_bidding',)


# Register your models here.
admin.site.register(DocumentType)
admin.site.register(Document)
