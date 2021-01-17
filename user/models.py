from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.forms import ModelForm
from ecomapp.models.shop import Product, Variants
from city.models import City
from warehouse.models import Warehouse
from home.models import Language
from currencies.models import Currency
from django.utils.safestring import mark_safe


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Користувач'))
    email = models.EmailField(
        blank=True,
        verbose_name=_("Електронна пошта"))
    phone = models.CharField(
        max_length=40,
        blank=True, null=True,
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
    country = models.CharField(
        blank=True,
        max_length=50,
        verbose_name=_('Країна'))
    city = models.ForeignKey(
        City, models.SET_NULL,
        blank=True, null=True, editable=True,
        verbose_name=_('Місто'))
    street = models.CharField(
        max_length=30,
        blank=True,
        editable=True,
        verbose_name=_('Вулиця'))
    house = models.CharField(
        max_length=30,
        blank=True,
        editable=True,
        verbose_name=_('Будинок'))
    apartment = models.CharField(
        max_length=30,
        blank=True,
        editable=True,
        verbose_name=_('Квартира / офіс'))
    warehouse_number = models.ForeignKey(
        Warehouse, models.SET_NULL,
        blank=True, null=True, editable=True,
        verbose_name=_('Номер відділення Нової пошти'))
    image = models.ImageField(
        blank=True,
        upload_to='Users',
        validators=[
            FileExtensionValidator(allowed_extensions=['svg', 'png', 'jpg', 'jpeg', 'webp'])],
        verbose_name=_('Аватарка'))
    is_active = models.BooleanField(default=False)
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name=_("Мова"))
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name=_("Валюта"))
    created = models.DateTimeField(
        default=now, verbose_name=_("Створено"))
    updated = models.DateTimeField(
        default=now, verbose_name=_("Оновлено") )

    class Meta:
        ordering = ['-created']
        verbose_name = _('Користувач')
        verbose_name_plural = _('Користувачі')

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' [' + self.user.username + '] '

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""
    image_tag.short_description = 'Image'


class UserWishlist(models.Model):
    parent = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL, null=True,
        related_name='wishes',
        verbose_name=_('Користувач'))
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='wishes',
        verbose_name=_('Товар'))
    variant = models.ForeignKey(
        Variants, on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_('Варіанти товару'))
    quantity = models.PositiveIntegerField(
        default=1, verbose_name=_('Кількість'))
    created = models.DateTimeField(
        _('created'), auto_now_add=True)
    updated = models.DateTimeField(
        _('updated'), auto_now=True)

    class Meta:
        verbose_name = _('Список бажань')
        verbose_name_plural = _('Список бажань')
        ordering = ['-created']
        unique_together = ('parent', 'product')

    def __str__(self):
        return self.product.name

    @property
    def price(self):
        return (self.product.price)


class UserWishlistForm(ModelForm):
    class Meta:
        model = UserWishlist
        fields = ['quantity']


class UserSignup(models.Model):
    parent = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='signup',
        verbose_name=_('Користувач'))
    email = models.EmailField(
        blank=True,
        verbose_name=_("Електронна пошта"))
    timestamp = models.DateTimeField(auto_now_add=True)
    is_subscribed = models.BooleanField(
        default=False,
        verbose_name=_('Підписка оформлена'))

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('Підписка')
        verbose_name_plural = _('Підписка')
        ordering = ['-timestamp']
