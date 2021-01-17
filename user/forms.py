from collections import OrderedDict
from django import forms
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from user.models import UserProfile, UserSignup
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
import re
from dal import autocomplete


class UserLoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        # USERNAME
        self.fields['username'].label = _('Логін')
        self.fields['username'].required = True
        self.fields['username'].widget.attrs['placeholder'] = _("Ім'я користувача або e-mail")
        self.fields['username'].widget.attrs['class'] = 'w3-input w3-border'
        # PASSWORD
        self.fields['password'].label = _('Пароль')
        self.fields['password'].required = True
        self.fields['password'].widget.attrs['placeholder'] = _("Пароль")
        self.fields['password'].widget.attrs['class'] = 'w3-input w3-border'


class UserRegistrationForm(forms.ModelForm):

    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'w3-input w3-border'
        # EMAIL
        self.fields['email'].label = 'E-mail'
        self.fields['email'].required = True
        self.fields['email'].widget.attrs['placeholder'] = _("E-mail адреса")
        # USERNAME
        self.fields['username'].label = _('Логін')
        self.fields['username'].help_text = _('Не більше 150 символів. Тільки букви, цифри і символи @/./+/-/_.')
        self.fields['username'].required = True
        self.fields['username'].widget.attrs['placeholder'] = _("Ім'я користувача")
        # FIRST NAME
        self.fields['first_name'].label = _("Ім'я")
        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs['placeholder'] = _("Ім'я")
        # LAST NAME
        self.fields['last_name'].label = _('Прізвище')
        self.fields['last_name'].required = True
        self.fields['last_name'].widget.attrs['placeholder'] = _('Прізвище')
        # PASSWORD1
        self.fields['password1'].label = _('Пароль')
        self.fields['password1'].required = True
        self.fields['password1'].widget.attrs['placeholder'] = _("Пароль")
        # PASSWORD2
        self.fields['password2'].label = _('Повторіть пароль')
        self.fields['password2'].required = True
        self.fields['password2'].widget.attrs['placeholder'] = _("Повторіть пароль")

    def clean(self):
        username = self.cleaned_data['username']
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        email = self.cleaned_data['email']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('Користувач з даним логіном вже зареєстрований!'))
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Користувач з даним поштовим адресом вже зареєстрований!'))
        if password1 != password2:
            raise forms.ValidationError(_('Ваші паролі не збігаються! Спробуйте знову.'))


class FormResetPassword(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super(FormResetPassword, self).__init__(*args, **kwargs)

        self.fields['email'].label = _('E-mail*')
        self.fields['email'].required = True
        self.fields['email'].widget.attrs['placeholder'] = _("E-mail")
        self.fields['email'].widget.attrs = {'class': 'w3-input w3-border'}


class FormSetPassword(SetPasswordForm):
    error_messages = {
        'password_mismatch': _("Введені два паролі не збігаються."),
        'password_notvalid': _("Пароль повинен містити 8 символів, які містять букви і цифри принаймні з 1 спеціальним символом та 1 великим регістром."),
    }
    new_password1 = forms.CharField(
        widget=forms.PasswordInput,
        strip=False
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super(FormSetPassword, self).__init__(*args, **kwargs)
        for field in ('new_password1', 'new_password2'):
            self.fields[field].widget.attrs = {'class': 'w3-input w3-border'}
        # NEW PASSWORD1
        self.fields['new_password1'].label = _('Новий пароль')
        self.fields['new_password1'].help_text = mark_safe(_('Ваш пароль не може бути занадто схожим на вашу іншу особисту інформацію.<br />'
                                                             'Ваш пароль повинен містити щонайменше 8 символів.<br />'
                                                             'Ваш пароль не може бути загальновживаним паролем.<br />'
                                                             'Ваш пароль не може бути повністю цифровим.'))
        self.fields['new_password1'].required = True
        self.fields['new_password1'].widget.attrs['placeholder'] = _("Новий пароль")
        # NEW PASSWORD2
        self.fields['new_password2'].label = _('Підтвердження нового паролю')
        self.fields['new_password2'].required = True
        self.fields['new_password2'].widget.attrs['placeholder'] = _("Підтвердження нового паролю")

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
            # Regix to check the password must contains sepcial char, numbers, char with upeercase and lowercase.
            regex = re.compile('((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%]).{8,30})')
            if (regex.search(password1) == None):
                raise forms.ValidationError(
                    self.error_messages['password_notvalid'],
                    code='password_mismatch',
                )

        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class FormChangePassword(FormSetPassword):

    error_messages = dict(FormSetPassword.error_messages, **{
        'password_incorrect': mark_safe(_("Ваш старий пароль було введено неправильно.<br/>"
                                          "Будь ласка, введіть його ще раз.")),
    })

    old_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(FormChangePassword, self).__init__(*args, **kwargs)
        for field in ('old_password', 'new_password1', 'new_password2'):
            self.fields[field].widget.attrs = {'class': 'w3-input w3-border'}
        # NEW PASSWORD1
        self.fields['new_password1'].label = _('Новий пароль')
        self.fields['new_password1'].help_text = mark_safe(
            _('Ваш пароль не може бути занадто схожим на вашу іншу особисту інформацію.<br />'
              'Ваш пароль повинен містити щонайменше 8 символів.<br />'
              'Ваш пароль не може бути загальновживаним паролем.<br />'
              'Ваш пароль не може бути повністю цифровим.'))
        self.fields['new_password1'].required = True
        self.fields['new_password1'].widget.attrs['placeholder'] = _("Новий пароль")
        # NEW PASSWORD2
        self.fields['new_password2'].label = _('Підтвердження нового паролю')
        self.fields['new_password2'].required = True
        self.fields['new_password2'].widget.attrs['placeholder'] = _("Підтвердження нового паролю")
        # OLD PASSWORD
        self.fields['old_password'].label = _('Старий пароль')
        self.fields['old_password'].required = True
        self.fields['old_password'].widget.attrs['placeholder'] = _("Старий пароль")

    def clean_old_password(self):

        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

    PasswordChangeForm.base_fields = OrderedDict(
        (k, PasswordChangeForm.base_fields[k])
        for k in ['old_password', 'new_password1', 'new_password2']
    )


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'input'
        # USERNAME
        self.fields['username'].label = _('Логін')
        self.fields['username'].help_text = _('Не більше 150 символів. Тільки букви, цифри і символи @/./+/-/_.')
        self.fields['username'].required = True
        self.fields['username'].widget.attrs['placeholder'] = _("Ім'я користувача або e-mail")
        # EMAIL
        self.fields['email'].label = 'E-mail'
        self.fields['email'].required = True
        self.fields['email'].widget.attrs['placeholder'] = _("E-mail адреса")
        # FIRST NAME
        self.fields['first_name'].label = _("Ім'я")
        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs['placeholder'] = _("Ім'я *")
        # LAST NAME
        self.fields['last_name'].label = _('Прізвище')
        self.fields['last_name'].required = True
        self.fields['last_name'].widget.attrs['placeholder'] = _('Прізвище *')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['father_name', 'phone', 'country', 'city', 'street', 'house', 'apartment', 'warehouse_number', 'image', 'language']

        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete'),
            'warehouse_number': autocomplete.ModelSelect2(url='warehouse-autocomplete')
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # FATHER NAME
        self.fields['father_name'].label = _("По батькові")
        self.fields['father_name'].required = False
        self.fields['father_name'].widget.attrs['placeholder'] = _("По батькові *")
        self.fields['father_name'].widget.attrs['class'] = 'input'
        # PHONE
        self.fields['phone'].label = _('Телефон')
        self.fields['phone'].help_text = _('*Вказуйте дійсний номер телефону')
        self.fields['phone'].required = True
        self.fields['phone'].widget.attrs['placeholder'] = _('Номер телефона *')
        self.fields['phone'].widget.attrs['class'] = 'input'
        # COUNTRY
        self.fields['country'].label = _('Країна')
        self.fields['country'].required = False
        self.fields['country'].widget.attrs['placeholder'] = _('Країна')
        self.fields['country'].widget.attrs['class'] = 'input'
        # CITY
        self.fields['city'].label = 'Місто'
        self.fields['city'].required = False
        self.fields['city'].widget.attrs['data-alert'] = _('Введіть місто доставки')
        self.fields['city'].widget.attrs['placeholder'] = _('Місто')
        self.fields['city'].widget.attrs['class'] = 'input'
        # STREET
        self.fields['street'].label = 'Вулиця'
        self.fields['street'].required = False
        self.fields['street'].widget.attrs['data-alert'] = _('Введіть назву вулиці')
        self.fields['street'].widget.attrs['placeholder'] = _('Вулиця*')
        self.fields['street'].widget.attrs['class'] = 'input'
        # HOUSE
        self.fields['house'].label = 'Будинок'
        self.fields['house'].required = False
        self.fields['house'].widget.attrs['data-alert'] = _('Введіть номер будинку')
        self.fields['house'].widget.attrs['placeholder'] = _('Номер будинку*')
        self.fields['house'].widget.attrs['class'] = 'input'
        # APARTMENT
        self.fields['apartment'].label = 'Квартира / офіс'
        self.fields['apartment'].required = False
        self.fields['apartment'].widget.attrs['data-alert'] = _('Введіть номер приміщення')
        self.fields['apartment'].widget.attrs['placeholder'] = _('Квартира / офіс')
        self.fields['apartment'].widget.attrs['class'] = 'input'
        # NUMBER
        self.fields['warehouse_number'].label = _('Склад Нової пошти')
        self.fields['warehouse_number'].required = False
        self.fields['warehouse_number'].widget.attrs['data-alert'] = _('Введіть номер відділення нової пошти')
        self.fields['warehouse_number'].widget.attrs['placeholder'] = _('Номер відділення')
        self.fields['warehouse_number'].widget.attrs['class'] = 'input'
        # IMAGE
        self.fields['image'].label = _('Аватарка')
        # LANGUAGE
        self.fields['language'].label = _('Мова')
        self.fields['language'].widget.attrs['class'] = 'input'


class EmailSignupForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        "class": "w3-input w3-border",
        "type": "email",
        "name": "email",
        "id": "email",
        "placeholder": "Введіть електронну пошту",
    }), label="")

    class Meta:
        model = UserSignup
        fields = ('email', )