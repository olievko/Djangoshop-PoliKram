from django.contrib.auth.models import User

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class Coupon(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, null=True,
        verbose_name=_("Користувач"))
    code = models.CharField(
        max_length=50, unique=True,
        verbose_name=_("Код"))
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_("Знижка"))
    active = models.BooleanField()

    class Meta:
        verbose_name = _("Купон")
        verbose_name_plural = _("Купони")

    def __str__(self):
        return self.code
