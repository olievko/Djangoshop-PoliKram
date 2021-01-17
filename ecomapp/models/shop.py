from django.db import models
from django.db.models import Avg, Count
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from django.contrib.auth.models import User
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from home.models import Language
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _


llist = Language.objects.all()
list1 = []
for rs in llist:
    list1.append((rs.code, rs.name))
langlist = (list1)


class Category(MPTTModel):

    class Meta:
        ordering = ['name']
        verbose_name = _('Категорія: українська мова')
        verbose_name_plural = _('Категорії: українська мова')

    parent = TreeForeignKey(
        'self', blank=True, null=True,
        related_name='children', on_delete=models.CASCADE)
    name = models.CharField(
        max_length=200,
        verbose_name=_("Назва категорії"))
    slug = models.SlugField(blank=True)
    icon = models.CharField(
        max_length=200, blank=True, null=True,
        verbose_name=_("Іконка категорії"))
    description = models.TextField(
        blank=True, verbose_name=_("Опис категорії"))
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField(
        max_length=255, blank=True, null=True,
        help_text=_('Розділений комами набір ключових слів SEO для метатегу ключових слів'))
    meta_description = models.CharField(
        max_length=255, blank=True, null=True,
        help_text=_('Контент для метатегу опис'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.slug])

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' / '.join(full_path[::-1])


class CategoryLang(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='categorylangs',
        on_delete=models.CASCADE,
        verbose_name=_("Категорія товарів"))
    lang = models.CharField(
        max_length=6, choices=langlist,
        verbose_name=_("Мова"))
    name = models.CharField(
        max_length=200,
        verbose_name=_("Назва категорії"))
    slug = models.SlugField(null=False, unique=True)
    description = RichTextUploadingField(
        blank=True, verbose_name=_("Опис категорії"))
    meta_keywords = models.CharField(
        max_length=255, blank=True, null=True,
        help_text=_('Розділений комами набір ключових слів SEO для метатегу ключових слів'))
    meta_description = models.CharField(
        max_length=255, blank=True, null=True,
        help_text=_('Контент для метатегу опис'))

    class Meta:
        ordering = ['name']
        verbose_name = _('Категорія: російська мова')
        verbose_name_plural = _('Категорії: російська мова')

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Country(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name=_('Назва країни виробника'))
    slug = models.SlugField(blank=True)

    class Meta:
        verbose_name = _('Країна виробник продукту')
        verbose_name_plural = _('Країни виробники продукту')

    def __str__(self):
        return self.name


class ActiveBrandManager(models.Manager):

    def get_query_set(self):
        return super(ActiveBrandManager, self).get_query_set().filter(is_active=True)


class Brand(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name=_('Назва бренду'))
    slug = models.SlugField(blank=True)
    description = models.TextField(
        blank=True,
        verbose_name=_("Опис бренду"))
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField(
        max_length=255, blank=True, null=True,
        help_text=_('Розділений комами набір ключових слів SEO для метатегу ключових слів'))
    meta_description = models.CharField(
        max_length=255, blank=True, null=True,
        help_text=_('Контент для метатегу опис'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active = ActiveBrandManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Бренд товару')
        verbose_name_plural = _('Бренди товарів')

    def __str__(self):
        return self.name


def image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return "{0}/{1}".format(instance.slug, filename)


class ActiveProductManager(models.Manager):
    def all(self):
        return super(ActiveProductManager, self).get_queryset().filter(available=True)


class Product(models.Model):

    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),
    )

    product_id = models.CharField(
        max_length=250, default='',
        verbose_name=_("Код товару"))
    category = models.ForeignKey(
        Category,
        related_name='products',
        blank=True, null=True,
        verbose_name=_("Категорія товару"),
        on_delete=models.PROTECT)
    brand = models.ForeignKey(
        Brand,
        related_name='products',
        blank=True, null=True,
        verbose_name=_("Бренд товару"),
        on_delete=models.PROTECT)
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        verbose_name=_("Країна виробник"),
        related_name='product',
        blank=True, null=True)
    name = models.CharField(
        max_length=200, null=True,
        verbose_name=_("Назва продукту"))
    slug = models.SlugField(max_length=200)
    articul = models.CharField(
        max_length=64, default='',
        verbose_name=_("Артикуль товару"))
    warranty = models.PositiveSmallIntegerField(
        default=6,
        verbose_name=_("Гарантія товару"),
        blank=True, null=True)
    image_url = models.URLField(
        blank=True, null=True,
        verbose_name=_("URL збраження"))
    image = models.ImageField(
        upload_to='ImagesMain',
        validators=[
            FileExtensionValidator(allowed_extensions=['svg', 'png', 'jpg', 'jpeg', 'webp'])],
        blank=True, null=True,
        verbose_name=_("Збраження товару"))
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(1000, 1000)],
        format='JPEG', options={'quality': 90})
    thumb = ImageSpecField(
        source='image',
        processors=[ResizeToFit(100, 100)],
        format='JPEG', options={'quality': 90})
    description = models.TextField(
        blank=True, verbose_name=_("Опис товару"))
    meta_keywords = models.CharField(
        _("Meta Keywords"),
        max_length=255, blank=True, null=True,
        help_text=_('Розділений комами набір ключових слів SEO для метатегу ключових слів'))
    meta_description = models.CharField(
        _("Meta Description"),
        max_length=255, blank=True, null=True,
        help_text=_('Контент для метатегу опис'))
    price = models.DecimalField(
        max_digits=9, decimal_places=2,
        verbose_name=_("Ціна"))
    old_price = models.DecimalField(
        max_digits=9, decimal_places=2,
        blank=True, default=0.00,
        verbose_name=_("Стара ціна"))
    stock = models.PositiveIntegerField(
        blank=True, default=1,
        verbose_name=_("На складі"))
    available = models.BooleanField(
        default=True, verbose_name=_("Доступний"))
    variant = models.CharField(
        max_length=10, choices=VARIANTS,
        default='None', verbose_name=_("Варіанти продукту"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active = ActiveProductManager()

    class Meta:
        ordering = ['created']
        index_together = [
            ['id', 'slug']
        ]
        verbose_name = _('Продукт: українська мова')
        verbose_name_plural = _('Продукти: українська мова')

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if self.image_url and not self.image:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.image_url).read())
            img_temp.flush()
            self.image.save(f"image_main_{self.id}", File(img_temp))
        super(Product, self).save(*args, **kwargs)

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])

    def avaregereview(self):
        reviews = ProductReview.approved.filter(product=self).aggregate(avarage=Avg('rating'))
        avg = 0
        if reviews["avarage"] is not None:
            avg = float(reviews["avarage"])
        return avg

    def countreview(self):
        reviews = ProductReview.approved.filter(product=self).aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt


class ProductLang(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("Продукт"))
    lang = models.CharField(
        max_length=6, choices=langlist)
    name = models.CharField(
        max_length=200, null=True,
        verbose_name=_("Назва продукту"))
    slug = models.SlugField(
        max_length=200,
        null=False, unique=True)
    description = RichTextUploadingField(
        blank=True, verbose_name=_("Опис"))
    meta_keywords = models.CharField(
        _("Meta Keywords"),
        max_length=255, blank=True, null=True,
        help_text=_('Розділений комами набір ключових слів SEO для метатегу ключових слів'))
    meta_description = models.CharField(
        _("Meta Description"),
        max_length=255, blank=True, null=True,
        help_text=_('Контент для метатегу опис'))

    class Meta:
        verbose_name = _('Продукт: російська мова')
        verbose_name_plural = _('Продукти: російська мова')

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


class Images(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_("Продукт"))
    image_url = models.URLField(
        blank=True, null=True,
        verbose_name=_("URL збраження"))
    image_file = models.ImageField(
        upload_to='ImagesGallery',
        validators=[
            FileExtensionValidator(allowed_extensions=['svg', 'png', 'jpg', 'jpeg', 'webp'])],
        blank=True, verbose_name=_("Додаткові збраження"))
    added = models.DateTimeField(
        auto_now_add=True, db_index=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Зображення продукту')
        verbose_name_plural = _('Зображення продукту')

    def save(self, *args, **kwargs):
        if self.image_url and not self.image_file:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.image_url).read())
            img_temp.flush()
            self.image_file.save(f"image_gallery_{self.id}", File(img_temp))
        super(Images, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images_detail', args=[self.id])


class ActiveProductReviewManager(models.Manager):
    def all(self):
        return super(ActiveProductReviewManager, self).all().filter(is_approved=True)


class ProductReview(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT,
        verbose_name=_("Продукт"))
    user = models.ForeignKey(
        User, on_delete=models.PROTECT,
        verbose_name=_("Користувач"))
    subject = models.CharField(
        max_length=50,
        verbose_name=_("Заголовок повідомлення"))
    rating = models.SmallIntegerField(
        default=1,
        verbose_name=_("Зірка"))
    is_approved = models.BooleanField(
        default=True,
        verbose_name=_("Затверджено"))
    content = models.TextField(
        blank=True,
        verbose_name=_("Повідомлення"))
    status = models.CharField(
        max_length=10,
        choices=STATUS, default='New')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    approved = ActiveProductReviewManager()

    class Meta:
        ordering = ['-created']
        verbose_name = _('Рейтинг продукту')
        verbose_name_plural = _('Рейтинги продукту')


class Color(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name=_("Назва кольору"))
    code = models.CharField(
        max_length=10,
        blank=True, null=True,
        verbose_name=_("Код кольору"))

    class Meta:
        verbose_name = _('Колір продукту')
        verbose_name_plural = _('Кольори продукту')

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""


class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(
        max_length=10,
        blank=True, null=True,
        verbose_name=_("Код"))

    class Meta:
        verbose_name = _('Розмір продукту')
        verbose_name_plural = _('Розміри продукту')

    def __str__(self):
        return self.name


class Variants(models.Model):
    title = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Назва варіанту"))
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("Продукт"))
    color = models.ForeignKey(
        Color,
        on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name=_("Колір продукту"))
    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name=_("Розмір продукту"))
    image_id = models.IntegerField(
        blank=True, null=True,
        default=0,
        verbose_name=_("Зображення_id"))
    quantity = models.IntegerField(
        default=1,
        verbose_name=_("На складі"))
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0,
        verbose_name=_("Ціна"))

    class Meta:
        verbose_name = _('Варіант продукту')
        verbose_name_plural = _('Варіанти продукту')

    def __str__(self):
        return self.title

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            varimage = img.image_file.url
        else:
            varimage = ""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(img.image_file.url))
        else:
            return ""