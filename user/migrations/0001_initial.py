# Generated by Django 3.0.6 on 2021-01-17 14:23

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('warehouse', '0001_initial'),
        ('city', '0001_initial'),
        ('currencies', '0006_increase_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0001_initial'),
        ('ecomapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Електронна пошта')),
                ('phone', models.CharField(blank=True, max_length=40, null=True, verbose_name='Телефон')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name="Ім'я")),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='Прізвище')),
                ('father_name', models.CharField(blank=True, max_length=30, verbose_name='По батькові')),
                ('country', models.CharField(blank=True, max_length=50, verbose_name='Країна')),
                ('street', models.CharField(blank=True, max_length=30, verbose_name='Вулиця')),
                ('house', models.CharField(blank=True, max_length=30, verbose_name='Будинок')),
                ('apartment', models.CharField(blank=True, max_length=30, verbose_name='Квартира / офіс')),
                ('image', models.ImageField(blank=True, upload_to='Users', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['svg', 'png', 'jpg', 'jpeg', 'webp'])], verbose_name='Аватарка')),
                ('is_active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Створено')),
                ('updated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Оновлено')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='city.City', verbose_name='Місто')),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='currencies.Currency', verbose_name='Валюта')),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Language', verbose_name='Мова')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Користувач')),
                ('warehouse_number', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='warehouse.Warehouse', verbose_name='Номер відділення Нової пошти')),
            ],
            options={
                'verbose_name': 'Користувач',
                'verbose_name_plural': 'Користувачі',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='UserSignup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Електронна пошта')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_subscribed', models.BooleanField(default=False, verbose_name='Підписка оформлена')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signup', to='user.UserProfile', verbose_name='Користувач')),
            ],
            options={
                'verbose_name': 'Підписка',
                'verbose_name_plural': 'Підписка',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='UserWishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Кількість')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wishes', to='user.UserProfile', verbose_name='Користувач')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishes', to='ecomapp.Product', verbose_name='Товар')),
                ('variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecomapp.Variants', verbose_name='Варіанти товару')),
            ],
            options={
                'verbose_name': 'Список бажань',
                'verbose_name_plural': 'Список бажань',
                'ordering': ['-created'],
                'unique_together': {('parent', 'product')},
            },
        ),
    ]
