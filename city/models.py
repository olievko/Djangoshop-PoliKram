from django.db import models
from django.utils.translation import ugettext_lazy as _


class City(models.Model):

    city_title = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name=_("Назва міста"))
    region = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name=_("Район"))
    area = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name=_("Область"))

    @property
    def full_name(self):
        return '{}, {} область'.format(self.city_title, self.area)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _('Місто')
        verbose_name_plural = _('Міста')
