from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth import (authenticate, password_validation)
from profile import models as profile_models
from django.contrib.auth.forms import UserChangeForm

User = get_user_model()


class SignupForm(ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')

    error_messages = {
        'password_mismatch': "Пароли не совпадают",
        'required': "Пожалуйста, заполните все поля для регистрации",
        'password_validation_error':
            "Пароль должен состоять из минимум 8 букв и цифр"
    }

    username_errors = {
        'required': "Введите логин",
        'unique': 'Такой логин уже существует'
    }

    email_errors = {
        'required': "Введите вашу почту",
        'invalid': "Введите корректную почту"
    }

    first_name_errors = {
        'required': "Введите ваше имя"
    }

    last_name_errors = {
        'required': "Введите вашу фамилию"
    }

    username = forms.CharField(label='Логин', error_messages=username_errors)
    email = forms.EmailField(label='Почта', error_messages=email_errors)
    first_name = forms.CharField(label='Имя', error_messages=first_name_errors)
    last_name = forms.CharField(
        label='Фамилия',
        error_messages=last_name_errors
        )
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Подтвердите пароль')

    def __init__(self, request=None, *args, **kwargs):
        """
        Кастомизация формы
        """
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        # first_name = self.cleaned_data.get('first_name')
        # last_name = self.cleaned_data.get('last_name')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        self.clean_unique(username, email)
        self.clean_password()

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch']
            )
        try:
            password_validation.validate_password(password1, self.instance)
        except forms.ValidationError:
            self.add_error(
                'password1',
                "Пароль должен состоять из минимум 8 букв и цифр"
            )
            # raise forms.ValidationError(
            # self.error_messages['password_validation_error']
            # )

    def clean_unique(self, username, email):
        User = get_user_model()
        usernames = User.objects.filter(username=username)
        emails = User.objects.filter(email=email)

        if usernames:
            self.add_error(
                'username',
                "Данный логин занят, используйте другой"
            )

        if emails:
            self.add_error('email', "Данная почта занята")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginForm(ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')

    # Общие ошибки для формы
    error_messages = {
        'invalid': 'Неправильный логин или пароль',
        'required': 'Пожалуйста, введите логин и пароль'
    }

    # Ошибки для поля логина
    username_errors = {
        'required': 'Введите ваш логин или почту'
    }

    # Ошибки для поля пароля
    password_errors = {
        'required': 'Введите пароль'
    }

    username = forms.CharField(
        label='username',
        error_messages=username_errors
    )
    password = forms.CharField(
        label='password',
        error_messages=password_errors
    )

    def __init__(self, request=None, *args, **kwargs):
        """
        Кастомизация формы
        """
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        login = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if login is None:
            raise self.get_required_error()

        if password is None:
            raise self.get_required_error()

        username = self.get_username(email=login)

        if username is not None:
            login = username

        user = authenticate(self.request, username=login, password=password)
        if user is None:
            raise self.get_invalid_error()
        self.user = user

    def get_invalid_error(self):
        return forms.ValidationError(
            self.error_messages['invalid'],
            code='invalid',
        )

    def get_required_error(self):
        return forms.ValidationError(
            self.error_messages['required'],
            code='required',
        )

    def get_username(self, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        else:
            return user.username

    def get_user(self):
        return self.user


class AdminSignupForm(ModelForm):

    class Meta:
        model = get_user_model()
        fields = (
                    'username', 'email', 'first_name',
                    'last_name', 'groups', 'company', 'password'
                 )

    error_messages = {
        'required':
            "Пожалуйста, заполните все поля для регистрации",
        'password_validation_error':
            "Пароль должен состоять из минимум 8 букв и цифр"
    }

    username_errors = {
        'required': "Введите логин",
        'unique': 'Такой логин уже существует'
    }

    email_errors = {
        'required': "Введите вашу почту",
        'invalid': "Введите корректную почту"
    }

    first_name_errors = {
        'required': "Введите ваше имя"
    }

    last_name_errors = {
        'required': "Введите вашу фамилию"
    }

    username = forms.CharField(label='Логин', error_messages=username_errors)
    email = forms.EmailField(label='Почта', error_messages=email_errors)
    first_name = forms.CharField(label='Имя', error_messages=first_name_errors)
    last_name = forms.CharField(
        label='Фамилия',
        error_messages=last_name_errors
        )
    password1 = forms.CharField(
            label='Пароль',
            required=True,
            widget=forms.PasswordInput()
        )
    password2 = forms.CharField(
        label='Подтвердите пароль',
        required=True,
        widget=forms.PasswordInput()
    )

    def __init__(self, *args, **kwargs):
        """
        Кастомизация формы
        """
        # self.request = kwargs['request']
        # self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        # first_name = self.cleaned_data.get('first_name')
        # last_name = self.cleaned_data.get('last_name')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        self.clean_unique(username, email)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password is None:
            self.add_error('password', 'Введите пароль')
        try:
            password_validation.validate_password(password, self.instance)
            self.password = password
        except forms.ValidationError:
            self.add_error(
                'password',
                "Пароль должен состоять из минимум 8 букв и цифр"
            )
            # raise forms.ValidationError(
            # self.error_messages['password_validation_error']
            # )

    def clean_unique(self, username, email):
        User = get_user_model()
        usernames = User.objects.filter(username=username)
        emails = User.objects.filter(email=email)

        if usernames:
            self.add_error(
                'username',
                "Данный логин занят, используйте другой"
            )

        if emails:
            self.add_error('email', "Данная почта занята")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user


class AdminUserChangeForm(UserChangeForm):
    company = forms.ModelChoiceField(
        queryset=profile_models.Company.objects.all(),
        required=False,
        label="Компания"
    )
