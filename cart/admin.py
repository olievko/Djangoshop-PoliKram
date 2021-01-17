from django.contrib import admin
from cart.models import CartItem, Cart


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'quantity', 'price']
    list_filter = ['user']


class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'coupon']
    list_filter = ['user']


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)