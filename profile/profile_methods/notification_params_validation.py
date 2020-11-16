from profile import forms
from profile import models



def polymer_notification_validation(polymer_notifications, user):
    for poly_notify in polymer_notifications:
        if not poly_notify['value']:
            if models.PolymerNotifications.objects.filter(client=user, polymer_id=poly_notify['id']).exists():
                models.PolymerNotifications.objects.filter(client=user, polymer_id=poly_notify['id']).delete()
        else:
            if not models.PolymerNotifications.objects.filter(client=user, polymer_id=poly_notify['id']).exists():
                form = forms.PolymerNotificationForm({'polymer_id': poly_notify['id'], 'client': user.id})
                if form.is_valid():
                    form.save()
                else:
                    print(form.errors)
                    return "Ошибка валидации"

    return None


def get_bool_value_in_num(js_str_bool):
    if js_str_bool == 'true':
        return True
    elif js_str_bool == 'false':
        return False
    else:
        return None
