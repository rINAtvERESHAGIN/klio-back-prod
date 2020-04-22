# Generated by Django 2.2.7 on 2020-04-19 23:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0026_auto_20200406_0138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userproduct',
            name='selected',
        ),
        migrations.AlterField(
            model_name='userproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selected_by', to='products.Product', verbose_name='product'),
        ),
        migrations.AlterField(
            model_name='userproduct',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
