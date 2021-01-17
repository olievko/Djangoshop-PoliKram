# -*- coding: utf-8 -*-
from django import forms
from cart.models import CartItem


class ShopCartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']
