# Generated by Django 2.2.7 on 2020-07-20 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0050_auto_20200628_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Do not set the price on a parent product.', max_digits=15, null=True, verbose_name='price'),
        ),
    ]
