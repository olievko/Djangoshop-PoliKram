from django.contrib import admin
from coupons.models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'valid_from', 'valid_to', 'discount', 'active']
    list_filter = ['user', 'active', 'valid_from', 'valid_to']
    search_fields = ['code']
