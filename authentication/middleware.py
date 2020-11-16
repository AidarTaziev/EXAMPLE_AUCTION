from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from profile.models import Company, OrganizationBranch
from django.conf import settings
from django.contrib.auth import login

import requests
import time

User = get_user_model()


class SyncUsersMiddleware(MiddlewareMixin):

    def process_request(self, request):
        from authentication.auth_methods import auth_logout
        if settings.PASSPORT_SESSION_ID_NAME not in request.COOKIES:
            if request.user.is_authenticated:
                return auth_logout(request)
        elif not request.user.is_authenticated:
            passport_user = get_user_from_passport(
                session_id=request.COOKIES[settings.PASSPORT_SESSION_ID_NAME])
            if passport_user:
                local_user = update_or_create_user(passport_user)
                login(request, local_user)
        else:
            passport_user = get_user_from_passport(session_id=request.COOKIES[settings.PASSPORT_SESSION_ID_NAME])
            if passport_user:
                passport_user_id = passport_user.get('user').get('id')
                local_user = update_or_create_user(passport_user)
                if request.user.id != passport_user_id:
                    login(request, local_user)
            else:
                return auth_logout(request)


def get_user_from_passport(user_id=None, session_id=None):
    data = {
        'session_id': session_id,
        'user_id': user_id,
        'secret': settings.PASSPORT_SECRET_KEY,
    }
    try:
        response = requests.post(settings.PASSPORT_USER_CREDENTIALS_URI, data=data)
    except requests.exceptions.RequestException as e:
        print(e)
        return None

    if response.status_code == 200:
        data = response.json()
        if not data['error']:
            return data['data']
    return None


def update_or_create_user(data):
    passport_company = data.get('company', None)
    user_company = None
    if passport_company:

        default_company_branch = {
            'id': 1,
            'name': 'Полимеры'
        }
        passport_branch = passport_company.get('branch', None) or default_company_branch
        branch = update_or_create(passport_branch, OrganizationBranch)
        passport_company['branch'] = branch
        user_company = update_or_create(passport_company, Company)

    user = update_or_create(data.get('user'), User)
    user.company = user_company
    user.save()
    return user


def update_or_create(data, model):
    pk = data.get('id')
    queryset = model.objects.filter(pk=pk)
    if queryset.exists():
        del data['id']
        queryset.update(**data)
        saved_instance = queryset[0]

    else:
        saved_instance = model.objects.create(**data)
    return saved_instance


def sync_user(user_id):
    passport_user = get_user_from_passport(user_id=user_id)
    if passport_user:
        user = update_or_create_user(passport_user)
        return user
    return None


# def update_or_create_branch(passport_branch):
#     branch_id = passport_branch.get('id')
#     branch = OrganizationBranch.objects.filter(pk=branch_id)
#     if branch.exists():
#         saved_branch = branch.update(**passport_branch)[0]
#     else:
#         saved_branch = OrganizationBranch.objects.create(**passport_branch)
#
#     return saved_branch
#
#
# def update_or_create_company(passport_company):
#     company_id = passport_company.get('id')
#     company = Company.objects.filter(pk=company_id)
#     if company.exists():
#         saved_company = company.update(**passport_company)
#     else:
#         saved_company = Company.objects.create(**passport_company)
#
#     return saved_company

# def user_in_db(user_id):
#     return User.objects.filter(pk=user_id).exists()


# def get_user_id_from_passport(session_id):
#     data = {
#         'session_id': session_id,
#         'secret': settings.PASSPORT_SECRET_KEY,
#     }
#     response = requests.post(settings.PASSPORT_USER_ID_URI, data=data)
#     if response.status_code == 200:
#         data = response.json()
#         if not data['error']:
#             return data['data']
#
#     return None

# def update_or_create_user(passport_user_credentials):
#     company = passport_user_credentials['company']
#     user_company = None
#
#     if company:
#         company_qs = Company.objects.filter(id=company['id'])
#         if company_qs.exists():
#             user_company = company_qs[0]
#         else:
#             if company['branch']:
#                 branch = OrganizationBranch.objects.get(pk=company['branch'])
#                 del company['branch']
#             else:
#                 branch = OrganizationBranch.objects.get(pk=0)
#
#             company['branch'] = branch
#             new_company = Company(**company)
#             user_company = new_company.save()
#
#     user = User.objects.update_or_create()
#     user.company = user_company
#
#     return user.save()