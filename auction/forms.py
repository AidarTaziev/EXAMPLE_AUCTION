import logging
from decimal import Decimal
from datetime import timedelta
from django import forms
from django.forms import ModelForm
from utils.time_customization.custom_time import current_datetime
from sprav.requests import get_polymer_short_info
from .models import Auction, AuctionParticipationOrder, AuctionSellerOffer, AuctionBet, AuctionDeal
s

class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['type', 'polymer_id', 'polymer_shortcode', 'polymer_type', 'polymer_type_id', 'polymer_plant', 'polymer_plant_id', 'lot_size', 'special_conditions',
                  'payment_term', 'step', 'shipment_condition', 'delivery', 'storage_location',
                  'start_bidding', 'end_bidding', 'fixation_duration', 'published_datetime', 'is_dev_bid', 'level', 'seller',
                  'is_template', 'is_apply_for_participation', 'is_price_with_nds', ]

    def clean(self):
        try:
            polymer_id = int(self.cleaned_data.get('polymer_id'))
            polymer_short_info = get_polymer_short_info(polymer_id)

            self.cleaned_data['polymer_shortcode'] = polymer_short_info['shortcode']
            self.cleaned_data['polymer_type'] = polymer_short_info['subtype__type__name']
            self.cleaned_data['polymer_type_id'] = polymer_short_info['subtype__type__id']
            if polymer_short_info['plants__name']:
                self.cleaned_data['polymer_plant'] = polymer_short_info['plants__name']
                self.cleaned_data['polymer_plant_id'] = polymer_short_info['plants__id']

            return self.cleaned_data
        except:
            raise forms.ValidationError('FORMS: lot_size not valid')

    def clean_lot_size(self):
        try:
            lot_size = float(self.cleaned_data.get('lot_size'))

            if lot_size <= 0:
                raise forms.ValidationError('FORMS: lot_size not valid')
        except:
            raise forms.ValidationError('FORMS: lot_size not valid')

        print('lot_size - ', lot_size)

        return lot_size

    def clean_step(self):
        try:
            step = int(self.cleaned_data.get('step'))

            if step <= 0:
                raise forms.ValidationError('FORMS: step not valid')
        except:
            raise forms.ValidationError('FORMS: step not valid')

        return step

    def clean_seller(self):
        try:
            seller = self.cleaned_data.get('seller')
            level = self.cleaned_data.get('level')
            users_groups = seller.groups.values_list('name', flat=True)

            if seller.company is None:
                raise forms.ValidationError('FORMS: seller not valid')
        except:
            raise forms.ValidationError('FORMS: seller not valid')

        return seller

    #TODO: ДОБАВИТЬ УСЛОВАИЕ CLEAN ДЛЯ START_BIDDING

    def clean_end_bidding(self):
        try:
            startAuction = self.cleaned_data.get('start_bidding')
            endAuction = self.cleaned_data.get('end_bidding')

            if endAuction < startAuction:
                raise forms.ValidationError('FORMS: Datetime of the endAuction less than datetime of startAuction')
        except:
            raise forms.ValidationError('FORMS: Datetime of the endAuction less than datetime of startAuction')

        return endAuction

    def clean_fixation_duration(self):
        try:
            fixation_duration = int(self.cleaned_data.get('fixation_duration'))

            if fixation_duration < 0:
                raise forms.ValidationError('FORMS: fixation_duration not valid')
        except:
            raise forms.ValidationError('FORMS: fixation_duration not valid')

        return fixation_duration

    def clean_seller(self):
        try:
            seller = self.cleaned_data.get('seller')
            level = self.cleaned_data.get('level')

            if seller.company is None:
                raise forms.ValidationError('FORMS: seller not valid')
        except:
            raise forms.ValidationError('FORMS: seller not valid')

        return seller

    def clean_published_datetime(self):

        return current_datetime()


class AuctionParticipationOrderForm(ModelForm):
    class Meta:
        model = AuctionParticipationOrder
        fields = ['auction', 'company', 'participation_status']


class AuctionSellersOffersForm(ModelForm):
    class Meta:
        model = AuctionSellerOffer
        fields = ['auction', 'lot_amount', 'total_amount', 'start_price_per_tone',
                  'middle_price_per_tone', 'stop_price_per_tone', 'published_datetime']

    def clean_lot_amount(self):
        try:
            lot_amount = int(self.cleaned_data.get('lot_amount'))

            if lot_amount <= 0:
                raise forms.ValidationError('FORMS: lot_amount not valid')
        except:
            raise forms.ValidationError('FORMS: lot_amount not valid')

        return lot_amount

    def clean_total_amount(self):
        try:
            auction = self.cleaned_data.get('EXAMPLE_AUCTION')
            lot_amount = int(self.cleaned_data.get('lot_amount'))

        except:
            raise forms.ValidationError('FORMS: totalAmount not valid')

        print('seller total amount', float(auction.lot_size * lot_amount))

        return float(auction.lot_size * lot_amount)

    def clean_start_price_per_tone(self):
        try:
            start_price_per_tone = int(self.cleaned_data.get('start_price_per_tone'))

            if start_price_per_tone <= 0:
                raise forms.ValidationError('FORMS: start_price_per_tone not valid')
        except:
            raise forms.ValidationError('FORMS: start_price_per_tone not valid')

        return start_price_per_tone

    def clean_middle_price_per_tone(self):
        try:
            middle_price_per_tone = int(self.cleaned_data.get('start_price_per_tone'))

            if middle_price_per_tone <= 0:
                raise forms.ValidationError('FORMS: middle_price_per_tone not valid')
        except:
            raise forms.ValidationError('FORMS: middle_price_per_tone not valid')

        return middle_price_per_tone

    def clean_stop_price_per_tone(self):
        try:
            auction = self.cleaned_data.get('EXAMPLE_AUCTION')
            if auction.type.name == 'Голландский':
                stop_price_per_tone = int(self.cleaned_data.get('stop_price_per_tone'))

                if stop_price_per_tone:
                    print(stop_price_per_tone, '---stop price per tone')
                    if stop_price_per_tone <= 0:
                        raise forms.ValidationError('FORMS: stop_price_per_tone not valid')
            else:
                return None
        except:
            raise forms.ValidationError('FORMS: stop_price_per_tone not valid')

        return stop_price_per_tone

    def clean_published_datetime(self):

        return current_datetime()


class AuctionBetForm(ModelForm):
    class Meta:
        model = AuctionBet
        fields = ['auction', 'lot_amount', 'bet_price_per_tone', 'total_amount',
                  'client', 'published_datetime', 'end_fixation_datetime', 'total_price']

    def clean_lot_amount(self):
        try:
            lot_amount = int(self.cleaned_data.get('lot_amount'))
            auction = self.cleaned_data.get('EXAMPLE_AUCTION')

            if lot_amount <= 0:
                raise forms.ValidationError('FORMS: lot_amount in bet not valid')

            if auction.type.name == 'Классический':
                auctionSellerOffer = auction.current_seller_offer
                if auctionSellerOffer.lot_amount < lot_amount:
                    raise forms.ValidationError('FORMS: num EXAMPLE_AUCTION bid lot amount < than lot amount in bet')
        except:

            raise forms.ValidationError('FORMS: parse lot amount exception')

        return lot_amount

    def clean_bet_price_per_tone(self):
        try:
            bet_price_per_tone = Decimal(self.cleaned_data.get('bet_price_per_tone'))
            auction = self.cleaned_data.get('EXAMPLE_AUCTION')

            if bet_price_per_tone <= 0:
                raise forms.ValidationError('FORMS: bet_price_per_tone not valid')

            if auction.type.name == 'Классический':
                auctionsellerOffer = auction.current_seller_offer
                if bet_price_per_tone < auctionsellerOffer.start_price_per_tone:
                    raise forms.ValidationError('FORMS: betPricePerTone less than EXAMPLE_AUCTION min bet price per tone')

        except:
            raise forms.ValidationError('FORMS: betPricePerTone is not Valid')

        return bet_price_per_tone

    def clean_total_amount(self):
        try:
            lot_amount = int(self.cleaned_data.get('lot_amount'))
            auction = self.cleaned_data.get('EXAMPLE_AUCTION')

        except:
            raise forms.ValidationError('FORMS: total amount is not int')

        print('bet total amount', float(auction.lot_size * lot_amount))


        return float(auction.lot_size) * lot_amount

    def clean_total_price(self):
        try:
            total_amount = int(self.cleaned_data.get('total_amount'))
            bet_price_per_tone = Decimal(self.cleaned_data.get('bet_price_per_tone'))
        except:
            raise forms.ValidationError('FORMS: clean_totalPrice exception')

        return bet_price_per_tone * total_amount

    def clean_published_datetime(self):

        return current_datetime()

    def clean_end_fixation_datetime(self):
        auction = self.cleaned_data.get('EXAMPLE_AUCTION')

        if auction.type.name == 'Классический' or auction.type.name == 'Голландский':
            return current_datetime() + timedelta(seconds=auction.fixation_duration)
        elif auction.type.name == 'Встречный':
            if auction.current_seller_offer:
                return current_datetime() + timedelta(seconds=auction.fixation_duration)


class AuctionDealForm(ModelForm):
    class Meta:
        model = AuctionDeal
        fields = ['bet', 'seller_offer', 'lot_amount', 'total_amount', 'published_datetime', 'total_price']

    def clean_lot_amount(self):
        bet = self.cleaned_data.get('bet')
        lot_amount = int(self.cleaned_data.get('lot_amount'))
        num_free_lots = bet.auction.num_free_lots

        if lot_amount <= 0:
            raise forms.ValidationError('FORMS: deal lot_amount in bet not valid')

        if num_free_lots:
            if num_free_lots < lot_amount:
                return num_free_lots
            else:
                return lot_amount
        else:
            raise forms.ValidationError('FORMS: deal lot_amount in bet not valid')

    def clean_total_amount(self):
        bet = self.cleaned_data.get('bet')
        lotAmount = int(self.cleaned_data.get('lot_amount'))
        return float(bet.auction.lot_size * lotAmount)

    def clean_total_price(self):
        total_amount = int(self.cleaned_data.get('total_amount'))
        bet = self.cleaned_data.get('bet')

        return bet.bet_price_per_tone * total_amount

    def clean_published_datetime(self):

        return current_datetime()

