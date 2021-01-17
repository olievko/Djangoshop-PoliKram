from django.db import models
from django.conf import settings
from ecomapp.models.shop import Product, Variants
from coupons.models import Coupon
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from city.models import City
from warehouse.models import Warehouse
from django.utils.translation import gettext_lazy as _


class Order(models.Model):

    ORDER_STATUSES = (
        (_('Прийнятий в обробку'), _('Прийнятий в обробку')),
        (_('Виконується'), _('Виконується')),
        (_('Відправлено'), _('Відправлено')),
        (_('Доставлено'), _('Доставлено')),
        (_('Відміненно'), _('Відміненно'))
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Користувач"))
    code = models.CharField(
        max_length=5, editable=False,
        verbose_name=_("Код замовлення"))
    email = models.EmailField(
        blank=True,
        verbose_name=_("Електронна пошта"))
    phone = models.CharField(
        max_length=40,
        blank=True,
        verbose_name=_("Телефон"))
    first_name = models.CharField(
        max_length=30,
        blank=True, editable=True,
        verbose_name=_("Ім'я"))
    last_name = models.CharField(
        max_length=30,
        blank=True, editable=True,
        verbose_name=_("Прізвище"))
    father_name = models.CharField(
        max_length=30,
        blank=True, editable=True,
        verbose_name=_('По батькові'))
    city = models.ForeignKey(
        City, models.SET_NULL,
        blank=True, null=True, editable=True,
        verbose_name=_('Місто'))
    order_option = models.CharField(
        max_length=40,
        choices=(
            ('user', _('Я')),
            ('other', _('Інший'))),
        default=_('Я'),
        verbose_name=_('Хто отримує замовлення?'))
    delivery_option = models.CharField(
        max_length=40,
        choices=(
            ('self', _('Склад Нової пошти')),
            ('delivery', _('Доставка на адресу'))),
        default=_('Склад Нової пошти'),
        verbose_name=_('Спосіб доставки'))
    street = models.CharField(
        max_length=250,
        blank=True, editable=True,
        verbose_name=_('Вулиця'))
    house = models.CharField(
        max_length=30,
        blank=True, editable=True,
        verbose_name=_('Будинок'))
    apartment = models.CharField(
        max_length=30,
        blank=True, editable=True,
        verbose_name=_('Квартира / офіс'))
    warehouse_number = models.ForeignKey(
        Warehouse, models.SET_NULL,
        blank=True, null=True, editable=True,
        verbose_name=_('Склад Нової Пошти'))
    payment_option = models.CharField(
        max_length=40,
        choices=(
            ('cash', _('Оплата при отриманні товару')),
            ('card', _('Картою онлайн')),),
        default=_('Оплата при отриманні товару'),
        verbose_name=_('Спосіб оплати'))
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Створено"))
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Оновлено"))
    comments = models.TextField(
        blank=True,
        verbose_name=_("Коментарії"))
    status = models.CharField(
        max_length=250,
        choices=ORDER_STATUSES,
        default=_("Прийнятий в обробку"),
        verbose_name=_('Статус'))
    paid = models.BooleanField(
        default=False,
        verbose_name=_("Сплачено"))
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_("Купон код"))
    discount = models.IntegerField(
        default=0,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_("Знижка, %"))

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Замовлення')
        verbose_name_plural = _('Замовлення')

    def __str__(self):
        return 'Заказ №{}'.format(str(self.id))

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost

    def get_discount(self):
        return self.get_total_cost() * (self.coupon.discount / Decimal('100'))

    def get_total_cost_after_discount(self):
        return self.get_total_cost() - self.get_discount()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_("Замовлення"))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        verbose_name=_("Користувач"))
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name=_("Товар"))
    variant = models.ForeignKey(
        Variants, on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_('Варіанти товару'))
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name=_("Ціна"))
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Кількість"))

    class Meta:
        verbose_name = _('Замовленний товар')
        verbose_name_plural = _('Замовленні товари')

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
