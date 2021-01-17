# Generated by Django 3.0.6 on 2021-01-17 14:23

import ckeditor_uploader.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Назва бренду')),
                ('slug', models.SlugField(blank=True)),
                ('description', models.TextField(blank=True, verbose_name='Опис бренду')),
                ('is_active', models.BooleanField(default=True)),
                ('meta_keywords', models.CharField(blank=True, help_text='Розділений комами набір ключових слів SEO для метатегу ключових слів', max_length=255, null=True)),
                ('meta_description', models.CharField(blank=True, help_text='Контент для метатегу опис', max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Бренд товару',
                'verbose_name_plural': 'Бренди товарів',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Назва категорії')),
                ('slug', models.SlugField(blank=True)),
                ('icon', models.CharField(blank=True, max_length=200, null=True, verbose_name='Іконка категорії')),
                ('description', models.TextField(blank=True, verbose_name='Опис категорії')),
                ('is_active', models.BooleanField(default=True)),
                ('meta_keywords', models.CharField(blank=True, help_text='Розділений комами набір ключових слів SEO для метатегу ключових слів', max_length=255, null=True)),
                ('meta_description', models.CharField(blank=True, help_text='Контент для метатегу опис', max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='ecomapp.Category')),
            ],
            options={
                'verbose_name': 'Категорія: українська мова',
                'verbose_name_plural': 'Категорії: українська мова',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Назва кольору')),
                ('code', models.CharField(blank=True, max_length=10, null=True, verbose_name='Код кольору')),
            ],
            options={
                'verbose_name': 'Колір продукту',
                'verbose_name_plural': 'Кольори продукту',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Назва країни виробника')),
                ('slug', models.SlugField(blank=True)),
            ],
            options={
                'verbose_name': 'Країна виробник продукту',
                'verbose_name_plural': 'Країни виробники продукту',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(default='', max_length=250, verbose_name='Код товару')),
                ('name', models.CharField(max_length=200, null=True, verbose_name='Назва продукту')),
                ('slug', models.SlugField(max_length=200)),
                ('articul', models.CharField(default='', max_length=64, verbose_name='Артикуль товару')),
                ('warranty', models.PositiveSmallIntegerField(blank=True, default=6, null=True, verbose_name='Гарантія товару')),
                ('image_url', models.URLField(blank=True, null=True, verbose_name='URL збраження')),
                ('image', models.ImageField(blank=True, null=True, upload_to='ImagesMain', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['svg', 'png', 'jpg', 'jpeg', 'webp'])], verbose_name='Збраження товару')),
                ('description', models.TextField(blank=True, verbose_name='Опис товару')),
                ('meta_keywords', models.CharField(blank=True, help_text='Розділений комами набір ключових слів SEO для метатегу ключових слів', max_length=255, null=True, verbose_name='Meta Keywords')),
                ('meta_description', models.CharField(blank=True, help_text='Контент для метатегу опис', max_length=255, null=True, verbose_name='Meta Description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Ціна')),
                ('old_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, verbose_name='Стара ціна')),
                ('stock', models.PositiveIntegerField(blank=True, default=1, verbose_name='На складі')),
                ('available', models.BooleanField(default=True, verbose_name='Доступний')),
                ('variant', models.CharField(choices=[('None', 'None'), ('Size', 'Size'), ('Color', 'Color'), ('Size-Color', 'Size-Color')], default='None', max_length=10, verbose_name='Варіанти продукту')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='ecomapp.Brand', verbose_name='Бренд товару')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='ecomapp.Category', verbose_name='Категорія товару')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='ecomapp.Country', verbose_name='Країна виробник')),
            ],
            options={
                'verbose_name': 'Продукт: українська мова',
                'verbose_name_plural': 'Продукти: українська мова',
                'ordering': ['created'],
                'index_together': {('id', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('code', models.CharField(blank=True, max_length=10, null=True, verbose_name='Код')),
            ],
            options={
                'verbose_name': 'Розмір продукту',
                'verbose_name_plural': 'Розміри продукту',
            },
        ),
        migrations.CreateModel(
            name='Variants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='Назва варіанту')),
                ('image_id', models.IntegerField(blank=True, default=0, null=True, verbose_name='Зображення_id')),
                ('quantity', models.IntegerField(default=1, verbose_name='На складі')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Ціна')),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecomapp.Color', verbose_name='Колір продукту')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomapp.Product', verbose_name='Продукт')),
                ('size', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecomapp.Size', verbose_name='Розмір продукту')),
            ],
            options={
                'verbose_name': 'Варіант продукту',
                'verbose_name_plural': 'Варіанти продукту',
            },
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50, verbose_name='Заголовок повідомлення')),
                ('rating', models.SmallIntegerField(default=1, verbose_name='Зірка')),
                ('is_approved', models.BooleanField(default=True, verbose_name='Затверджено')),
                ('content', models.TextField(blank=True, verbose_name='Повідомлення')),
                ('status', models.CharField(choices=[('New', 'New'), ('True', 'True'), ('False', 'False')], default='New', max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ecomapp.Product', verbose_name='Продукт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Користувач')),
            ],
            options={
                'verbose_name': 'Рейтинг продукту',
                'verbose_name_plural': 'Рейтинги продукту',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ProductLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang', models.CharField(choices=[('uk', 'Українська'), ('ru', 'Русский')], max_length=6)),
                ('name', models.CharField(max_length=200, null=True, verbose_name='Назва продукту')),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='Опис')),
                ('meta_keywords', models.CharField(blank=True, help_text='Розділений комами набір ключових слів SEO для метатегу ключових слів', max_length=255, null=True, verbose_name='Meta Keywords')),
                ('meta_description', models.CharField(blank=True, help_text='Контент для метатегу опис', max_length=255, null=True, verbose_name='Meta Description')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomapp.Product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Продукт: російська мова',
                'verbose_name_plural': 'Продукти: російська мова',
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(blank=True, null=True, verbose_name='URL збраження')),
                ('image_file', models.ImageField(blank=True, upload_to='ImagesGallery', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['svg', 'png', 'jpg', 'jpeg', 'webp'])], verbose_name='Додаткові збраження')),
                ('added', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('is_active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='ecomapp.Product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Зображення продукту',
                'verbose_name_plural': 'Зображення продукту',
            },
        ),
        migrations.CreateModel(
            name='CategoryLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang', models.CharField(choices=[('uk', 'Українська'), ('ru', 'Русский')], max_length=6, verbose_name='Мова')),
                ('name', models.CharField(max_length=200, verbose_name='Назва категорії')),
                ('slug', models.SlugField(unique=True)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='Опис категорії')),
                ('meta_keywords', models.CharField(blank=True, help_text='Розділений комами набір ключових слів SEO для метатегу ключових слів', max_length=255, null=True)),
                ('meta_description', models.CharField(blank=True, help_text='Контент для метатегу опис', max_length=255, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categorylangs', to='ecomapp.Category', verbose_name='Категорія товарів')),
            ],
            options={
                'verbose_name': 'Категорія: російська мова',
                'verbose_name_plural': 'Категорії: російська мова',
                'ordering': ['name'],
            },
        ),
    ]
