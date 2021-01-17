# Generated by Django 3.0.6 on 2021-01-17 14:23

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('warehouse', '0001_initial'),
        ('city', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coupons', '0001_initial'),
        ('ecomapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(editable=False, max_length=5, verbose_name='Код замовлення')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Електронна пошта')),
                ('phone', models.CharField(blank=True, max_length=40, verbose_name='Телефон')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name="Ім'я")),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='Прізвище')),
                ('father_name', models.CharField(blank=True, max_length=30, verbose_name='По батькові')),
                ('order_option', models.CharField(choices=[('user', 'Я'), ('other', 'Інший')], default='Я', max_length=40, verbose_name='Хто отримує замовлення?')),
                ('delivery_option', models.CharField(choices=[('self', 'Склад Нової пошти'), ('delivery', 'Доставка на адресу')], default='Склад Нової пошти', max_length=40, verbose_name='Спосіб доставки')),
                ('street', models.CharField(blank=True, max_length=250, verbose_name='Вулиця')),
                ('house', models.CharField(blank=True, max_length=30, verbose_name='Будинок')),
                ('apartment', models.CharField(blank=True, max_length=30, verbose_name='Квартира / офіс')),
                ('payment_option', models.CharField(choices=[('cash', 'Оплата при отриманні товару'), ('card', 'Картою онлайн')], default='Оплата при отриманні товару', max_length=40, verbose_name='Спосіб оплати')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Створено')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Оновлено')),
                ('comments', models.TextField(blank=True, verbose_name='Коментарії')),
                ('status', models.CharField(choices=[('Прийнятий в обробку', 'Прийнятий в обробку'), ('Виконується', 'Виконується'), ('Відправлено', 'Відправлено'), ('Доставлено', 'Доставлено'), ('Відміненно', 'Відміненно')], default='Прийнятий в обробку', max_length=250, verbose_name='Статус')),
                ('paid', models.BooleanField(default=False, verbose_name='Сплачено')),
                ('discount', models.IntegerField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Знижка, %')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='city.City', verbose_name='Місто')),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='coupons.Coupon', verbose_name='Купон код')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Користувач')),
                ('warehouse_number', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='warehouse.Warehouse', verbose_name='Склад Нової Пошти')),
            ],
            options={
                'verbose_name': 'Замовлення',
                'verbose_name_plural': 'Замовлення',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Ціна')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Кількість')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.Order', verbose_name='Замовлення')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='ecomapp.Product', verbose_name='Товар')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Користувач')),
                ('variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecomapp.Variants', verbose_name='Варіанти товару')),
            ],
            options={
                'verbose_name': 'Замовленний товар',
                'verbose_name_plural': 'Замовленні товари',
            },
        ),
    ]