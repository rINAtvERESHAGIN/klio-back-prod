# Generated by Django 2.2.7 on 2020-02-04 00:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities_light', '0008_city_timezone'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderPaymentInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('cash', 'Cash'), ('card', 'Plastic Card'), ('transfer', 'Wire transfer')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='OrderPrivateInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_type', models.CharField(choices=[('individual', 'Individual'), ('company', 'Company')], max_length=10)),
                ('last_name', models.CharField(default=None, max_length=64, null=True)),
                ('first_name', models.CharField(default=None, max_length=64, null=True)),
                ('middle_name', models.CharField(blank=True, default=None, max_length=128, null=True)),
                ('phone', models.CharField(default=None, max_length=64, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('personal_data', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('start_date', models.DateTimeField()),
                ('deadline', models.DateTimeField()),
                ('activity', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='OrderDeliveryInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('pickup', 'Pickup'), ('courier', 'Courier')], max_length=10)),
                ('comment', models.TextField(blank=True)),
                ('delivery_terms', models.BooleanField(default=False)),
                ('from_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contacts.Contact')),
                ('to_city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cities_light.City')),
                ('to_country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cities_light.Country')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('active', 'Order is active'), ('pending', 'Order pending'), ('completed', 'Order completed'), ('denied', 'Order denied')], max_length=10)),
                ('step', models.PositiveSmallIntegerField(default=1)),
                ('promo', models.BooleanField(default=False)),
                ('promo_code', models.CharField(blank=True, max_length=14)),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basket.Basket')),
                ('delivery_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='basket.OrderDeliveryInfo')),
                ('payment_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='basket.OrderPaymentInfo')),
                ('private_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='basket.OrderPrivateInfo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BasketProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basket.Basket')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
        migrations.AddField(
            model_name='basket',
            name='product',
            field=models.ManyToManyField(through='basket.BasketProduct', to='products.Product'),
        ),
        migrations.AddField(
            model_name='basket',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
