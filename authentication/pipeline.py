from profile.models import Company


def update_user(backend, user, response, *args, **kwargs):
    if backend.name == 'kartli-oauth2' and user:
        if not response['company']:
            user.company = None
        else:
            company_qs = Company.objects.filter(id=response['company']['id'])
            if company_qs.exists():
                company = company_qs[0]
            else:
                company = Company.objects.create(**response['company'])

            user.company = company

        user.username = response['username']
        user.email = response['email']
        user.first_name = response['first_name']
        user.last_name = response['last_name']
        user.save()