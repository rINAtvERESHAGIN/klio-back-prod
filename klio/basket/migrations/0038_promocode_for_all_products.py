# Generated by Django 2.2.7 on 2020-04-29 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0037_orderdeliveryinfo_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocode',
            name='for_all_products',
            field=models.BooleanField(blank=True, default=False, verbose_name='For all products'),
        ),
    ]
