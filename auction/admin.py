from django.contrib import admin
from auction.models import *


class MyAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])
        return app_list


class AuctionBidChangeFormAdmin(admin.ModelAdmin):
    fields = ('shipment_condition',  'delivery', 'storage_location',
              'lot_size', 'payment_term', 'step', 'start_bidding', 'end_bidding',)


admin.site = MyAdminSite()
admin.site.register(ShipmentConditions)
admin.site.register(ShipmentMethods)
admin.site.register(PaymentTerms)
# admin.site.register(AuctionLevel)
admin.site.register(Auction, AuctionBidChangeFormAdmin)
# admin.site.register(AuctionDeal, AuctionDealFormAdmin)
