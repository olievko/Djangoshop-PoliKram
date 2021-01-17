from django.contrib import admin
from user.models import UserWishlist, UserProfile, UserSignup
from django.utils.translation import gettext_lazy as _


class UserWishlistInline(admin.StackedInline):
    model = UserWishlist
    fk_name = "parent"
    extra = 0


class UserSignupInline(admin.StackedInline):
    model = UserSignup
    fk_name = "parent"
    extra = 0


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    inlines = [
        UserWishlistInline,
        UserSignupInline
    ]
    list_display = ('user', 'email', 'phone', 'first_name', 'last_name', 'created', 'is_active', 'image_tag')
    list_filter = ('is_active',)
    search_fields = ('email',)
    ordering = ['-created']
    filter_horizontal = ()
    fieldsets = (
        (_('Користувач'), {'fields': ('user', 'email', 'phone', 'first_name', 'last_name', 'father_name', 'country', 'image', 'created', 'updated')}),
        (_('Адреса доставки'), {'fields': ('city', 'street', 'house', 'apartment')}),
        (_('Склад Нової пошти'), {'fields': ('warehouse_number', )}),
        (_('Мова та Валюта'), {'fields': ('language', 'currency')}),
        (_('Статус'), {'fields': ('is_active',)}),
    )


class UserWishlistAdmin(admin.ModelAdmin):
    list_display = ['product', 'parent', 'quantity', 'price']
    list_filter = ['parent']


class UserSignupAdmin(admin.ModelAdmin):
    list_display = ['email', 'parent', 'is_subscribed']
    list_filter = ['parent']


admin.site.register(UserWishlist, UserWishlistAdmin)
admin.site.register(UserSignup)