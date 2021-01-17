from django.db import models
from django.conf import settings
from ecomapp.models.shop import Product, Variants
from coupons.models import Coupon
from decimal import Decimal
from django.utils.translation import gettext_lazy as _


class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True,
        verbose_name=_("Користувач"))
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL, null=True,
        verbose_name=_("Товар"))
    variant = models.ForeignKey(
        Variants,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_('Варіанти товару'))
    price = models.DecimalField(
        max_digits=9, decimal_places=2,
        verbose_name=_("Ціна"))
    quantity = models.PositiveIntegerField(
        verbose_name=_("Кількість"))

    class Meta:
        verbose_name = _("Вміст корзини")
        verbose_name_plural = _("Вміст корзини")

    def __str__(self):
        return self.product.name

    def total_price(self):
        return self.quantity * self.price


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Користувач"))
    items = models.ManyToManyField(
        CartItem, verbose_name=_("Товари"))
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_("Купон код"))

    class Meta:
        verbose_name = _("Корзина")
        verbose_name_plural = _("Корзина")

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for item in self.items.all():
            total += item.total_price()
        return total

    def get_discount(self):
        return self.get_total() * (self.coupon.discount / Decimal('100'))

    def get_total_after_discount(self):
        return self.get_total() - self.get_discount()
