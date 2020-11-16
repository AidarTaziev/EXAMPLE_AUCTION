from django.contrib.auth import get_user_model
from django import forms
from .models import PolymerNotifications
User = get_user_model()


class Profile(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('creating_auction_notification', 'starting_auction_notification', 'cancel_auction_notification',)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = request.user
        super().__init__(*args, **kwargs)

    def update(self):
        user_to_update = User.objects.filter(id=self.user.id)
        user_to_update.update(**self.cleaned_data)
        return user_to_update



class PolymerNotificationForm(forms.ModelForm):
    class Meta:
        model = PolymerNotifications
        fields = ['client', 'polymer_id']
