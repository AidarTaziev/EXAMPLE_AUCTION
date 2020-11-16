from django.forms import ValidationError

def inn_validator(inn):
    inn_len = len(inn)
    if inn is None:
        raise ValidationError('ИНН обязателен для заполнения', code='req')

    if inn_len!=10 and inn_len!=12 or not is_num(inn):
        raise ValidationError('Введите корректный ИНН, он должне состоять из 10 или 12 цифр', code='invalid_value')

    # Разбирение ИНН в массив для проверки контрольной суммы
    c = []
    try:
        for num in inn:
            c.append(int(num))
    except ValueError:
        raise ValidationError('ИНН может состоять только из цифр', code='invalid_value')

    check_sum_error_message = "Введите корректный ИНН, контрольные цифры не совпадают"
    if inn_len == 10:
        check_sum = ((2*c[0] + 4*c[1] + 10*c[2] + 3*c[3] + 5*c[4] + 9*c[5] +
        4*c[6] + 6*c[7] + 8*c[8]) % 11) % 10

        if check_sum!=c[9]:
            raise ValidationError(check_sum_error_message, code='invalid_value')
    else:
        check_sum11 = ((7*c[0] + 2*c[1] + 4*c[2] + 10*c[3] + 3*c[4] + 5*c[5] +
        9*c[6] + 4*c[7] + 6*c[8] + 8*c[9]) % 11) % 10

        if check_sum11 != c[10]:
            raise ValidationError(check_sum_error_message, code='invalid_value')

        check_sum12 = ((3*c[0] + 7*c[1] + 2*c[2] + 4*c[3] + 10*c[4] + 3*c[5] +
        5*c[6] + 9*c[7] + 4*c[8] + 6*c[9] + 8*check_sum11) % 11) % 10

        if check_sum12 != c[11]:
            raise ValidationError(check_sum_error_message, code='invalid_value')


# def inn_unique(inn):
#     company = Company.objects.filter(inn=inn)
#     if company:
#         raise ValidationError('Данный ИНН уже занят, ')


def phone_validator(phone):
    if phone is None:
        raise ValidationError('Номер телефона обязателен для заполнения', code='required')
    if len(phone) > 18:
        raise ValidationError('Введите корректный номер телефона', code='invalid')


def kpp_validator(kpp_int):
    kpp = str(kpp_int)
    if kpp is None:
        raise ValidationError('Введите КПП', code='required')

    if len(kpp) != 9 or not is_num(kpp):
        raise ValidationError('Проверьте введенный КПП, он должен состоять из 9 цифр', code='invalid')


def ogrn_validator(ogrn_int):
    ogrn = str(ogrn_int)
    if ogrn is None:
        raise ValidationError('Введите ОГРН', code='required')

    if len(ogrn) != 13 or not is_num(ogrn):
        raise ValidationError('Проверьте введеный ОГРН, он должен состоять из 13 цифр', code='qwe')

    ogrn_sum = ogrn[0:12]
    check_sum = int(ogrn_sum) % 11
    str_sum = str(check_sum)

    if check_sum > 9:
        str_sum =  str_sum[len(str_sum)-1]

    if str_sum != ogrn[12]:
        raise ValidationError('Проверьте правильность ввода ОГРН, контрольные числа не совпадают',
            code='invalid')


def okato_validator(okato_int):
    okato = str(okato_int)
    if okato is None:
        raise ValidationError('Введите ОКАТО', code='required')
    if len(okato) < 8 or not is_num(okato):
        raise ValidationError('Введите корректный ОКАТО, он состоит из цифр', code='invalid')


def bik_validator(bik_int):
    bik = str(bik_int)
    if bik is None:
        raise ValidationError('Введите БИК', code='required')

    if len(bik) != 9 or not is_num(bik):
        raise ValidationError('Введите корректный БИК, он должен состоять из 9 цифр', code='invalid')


def account_validator(acc_int):
    acc = str(acc_int)
    if acc is None:
        raise ValidationError('Введите счет', code='required')
    if len(acc)!=20 or not is_num(acc):
        raise ValidationError('Введите корректный счет, он должен состоять из 20 цифр', code='invalid')


def postcode_validator(postcode_int):
    postcode = str(postcode_int)
    if postcode is None:
        raise ValidationError('Введите почтовый индект', code='required')
    if len(postcode) != 6 or not is_num(postcode):
        raise ValidationError('Введите коррект почтовый индекс, он должен состоять из 6 цифр', code='invalid')


def is_num(value):
    try:
        int(value)
        return True
    except ValueError:
        return False
