# -*- coding: utf-8 -*-
from django import forms
from orders.models import Order
from dal import autocomplete


class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['order_option',
                  'email',
                  'phone',
                  'first_name',
                  'last_name',
                  'father_name',
                  'city',
                  'delivery_option',
                  'street',
                  'house',
                  'apartment',
                  'warehouse_number',
                  'payment_option',
                  'comments']

        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete'),
            'warehouse_number': autocomplete.ModelSelect2(url='warehouse-autocomplete')
        }

    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'input'})
        # ORDER OPTION
        self.fields['order_option'].label = ''
        self.fields['order_option'].required = True
        self.fields['order_option'].widget.attrs['data-alert'] = 'Хто отримує замовлення?'
        self.fields['order_option'].widget = forms.Select(attrs={"class": "input"})
        self.fields['order_option'].choices = (('user', 'Я'), ('other', 'Інший'))
        # EMAIL
        self.fields['email'].label = ''
        self.fields['email'].help_texts = '*Вказуйте дійсну електронну пошту'
        self.fields['email'].required = False
        self.fields['email'].widget.attrs['data-alert'] = 'Введіть Ваш Email'
        self.fields['email'].widget.attrs['data-error'] = 'Email має не правильний формат'
        self.fields['email'].widget.attrs['placeholder'] = 'Email*'
        # PHONE
        self.fields['phone'].label = ''
        self.fields['phone'].help_texts = '*Вказуйте дійсний номер телефону'
        self.fields['phone'].required = False
        self.fields['phone'].widget.attrs['data-alert'] = 'Введіть Номер телефону'
        self.fields['phone'].widget.attrs['placeholder'] = 'Номер телефону*'
        # FIRST NAME
        self.fields['first_name'].label = ""
        self.fields['first_name'].required = False
        self.fields['first_name'].widget.attrs['data-alert'] = "Ваше Ім'я"
        self.fields['first_name'].widget.attrs['placeholder'] = "Ім'я*"
        # LAST NAME
        self.fields['last_name'].label = ''
        self.fields['last_name'].required = False
        self.fields['last_name'].widget.attrs['data-alert'] = 'Ваше Прізвище'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Прізвище*'
        # FATHER NAME
        self.fields['father_name'].label = ''
        self.fields['father_name'].required = False
        self.fields['father_name'].widget.attrs['data-alert'] = 'По батькові'
        self.fields['father_name'].widget.attrs['placeholder'] = 'По батькові'
        # CITY
        self.fields['city'].label = ''
        self.fields['city'].required = False
        self.fields['city'].widget.attrs['data-alert'] = 'Введіть місто доставки'
        self.fields['city'].widget.attrs['data-placeholder'] = 'Місто*'
        # DELIVERY OPTION
        self.fields['delivery_option'].label = ''
        self.fields['delivery_option'].required = True
        self.fields['delivery_option'].widget.attrs['data-alert'] = 'Спосіб отримання'
        self.fields['delivery_option'].widget = forms.Select(attrs={"class": "input"})
        self.fields['delivery_option'].choices = (('self', 'Склад Нової пошти'), ('delivery', 'Доставка на адресу'))
        # STREET
        self.fields['street'].label = ''
        self.fields['street'].required = False
        self.fields['street'].widget.attrs['data-alert'] = 'Введіть назву вулиці'
        self.fields['street'].widget.attrs['placeholder'] = 'Вулиця'
        # HOUSE
        self.fields['house'].label = ''
        self.fields['house'].required = False
        self.fields['house'].widget.attrs['data-alert'] = 'Введіть номер будинку'
        self.fields['house'].widget.attrs['placeholder'] = 'Номер будинку'
        # APARTMENT
        self.fields['apartment'].label = ''
        self.fields['apartment'].required = False
        self.fields['apartment'].widget.attrs['data-alert'] = 'Введіть номер приміщення'
        self.fields['apartment'].widget.attrs['placeholder'] = 'Квартира / офіс'
        # WAREHOUSE NUMBER
        self.fields['warehouse_number'].label = ''
        self.fields['warehouse_number'].required = False
        self.fields['warehouse_number'].widget.attrs['data-alert'] = 'Введіть номер відділення нової пошти'
        self.fields['warehouse_number'].widget.attrs['data-placeholder'] = 'Склад Нової пошти'
        # PAYMENT OPTION
        self.fields['payment_option'].label = ''
        self.fields['payment_option'].required = True
        self.fields['payment_option'].widget.attrs['data-alert'] = 'Спосіб оплати'
        self.fields['payment_option'].widget = forms.RadioSelect()
        self.fields['payment_option'].choices = (('cash', 'Оплата при отриманні товару'), ('card', 'Картою онлайн'))
        # COMMENTS
        self.fields['comments'].label = ''
        self.fields['comments'].required = False
        self.fields['comments'].widget.attrs['data-alert'] = 'Введіть повідомлення'
        self.fields['comments'].widget.attrs['placeholder'] = 'Повідомлення'
        self.fields['comments'].widget = forms.TextInput(attrs={'size': '40', 'class': 'w3-input w3-border'})

