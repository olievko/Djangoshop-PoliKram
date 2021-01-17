from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.translation import gettext_lazy as _


class Language(models.Model):
    name = models.CharField(
        max_length=20, verbose_name=_("Мова"))
    code = models.CharField(
        max_length=5, verbose_name=_("Код"))
    status = models.BooleanField(verbose_name=_("Статус"))
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Мова')
        verbose_name_plural = _('Мова')

    def __str__(self):
        return self.name


llist = Language.objects.filter(status=True)
list1 = []
for rs in llist:
    list1.append((rs.code, rs.name))
langlist = (list1)


class Setting(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField(
        max_length=150,
        verbose_name=_("Назва"))
    keywords = models.CharField(
        max_length=255,
        verbose_name=_("Ключові слова"))
    description = models.CharField(
        max_length=255,
        verbose_name=_("Опис"))
    company = models.CharField(
        max_length=50,
        verbose_name=_("Компанія"))
    address = models.CharField(
        blank=True, max_length=100,
        verbose_name=_("Адреса"))
    phone = models.CharField(
        blank=True, max_length=15,
        verbose_name=_("Телефон"))
    fax = models.CharField(
        blank=True, max_length=15,
        verbose_name=_("Факс"))

    email = models.CharField(
        blank=True, max_length=50)
    smtpserver = models.CharField(
        blank=True, max_length=50)
    smtpemail = models.CharField(
        blank=True, max_length=50)
    smtppassword = models.CharField(
        blank=True, max_length=10)
    smtpport = models.CharField(
        blank=True, max_length=5)
    icon = models.ImageField(
        blank=True, upload_to='images/',
        verbose_name=_("Іконка"))

    facebook = models.CharField(
        blank=True, max_length=50)
    instagram = models.CharField(
        blank=True, max_length=50)
    twitter = models.CharField(
        blank=True, max_length=50)
    youtube = models.CharField(
        blank=True, max_length=50)

    aboutus = RichTextUploadingField(
        blank=True,
        verbose_name=_('Про компанію'))
    shipmentpayment = RichTextUploadingField(
        blank=True,
        verbose_name=_('Доставка та Оплата'))
    warranty = RichTextUploadingField(
        blank=True,
        verbose_name=_('Гарантія'))
    purchasereturn = RichTextUploadingField(
        blank=True,
        verbose_name=_('Повернення товару'))
    status = models.CharField(
        max_length=10, choices=STATUS,
        verbose_name=_("Статус"))
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Налаштування: українська мова")
        verbose_name_plural = _("Налаштування: українська мова")

    def __str__(self):
        return self.title


class SettingLang(models.Model):

    setting = models.ForeignKey(
        Setting, on_delete=models.CASCADE,
        verbose_name=_("Налаштування"))
    lang = models.CharField(
        max_length=6, choices=langlist,
        verbose_name=_("Мова"))

    title = models.CharField(
        max_length=150, verbose_name=_("Назва"))
    keywords = models.CharField(
        max_length=255, verbose_name=_("Ключові слова"))
    description = models.CharField(
        max_length=255, verbose_name=_("Опис"))

    aboutus = RichTextUploadingField(
        blank=True, verbose_name=_('Про компанію'))
    shipmentpayment = RichTextUploadingField(
        blank=True, verbose_name=_('Доставка та Оплата'))
    warranty = RichTextUploadingField(
        blank=True, verbose_name=_('Гарантія'))
    purchasereturn = RichTextUploadingField(
        blank=True, verbose_name=_('Повернення товару'))

    class Meta:
        verbose_name = _("Налаштування: російська мова")
        verbose_name_plural = _("Налаштування: російська мова")

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    contact_name = models.CharField(
        blank=True, max_length=20,
        verbose_name=_("Контактне ім'я"))
    email = models.CharField(
        blank=True, max_length=50)
    subject = models.CharField(
        blank=True, max_length=50,
        verbose_name=_("Тема повідомлення"))
    comment = models.TextField(
        blank=True, max_length=255,
        verbose_name=_("Текст повідомлення"))
    status = models.CharField(
        max_length=10, choices=STATUS,
        verbose_name=_("Статус"), default='New')
    note = models.CharField(
        blank=True, max_length=100,
        verbose_name=_("Примітка"))
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Повідомлення")
        verbose_name_plural = _("Повідомлення")

    def __str__(self):
        return self.contact_name
