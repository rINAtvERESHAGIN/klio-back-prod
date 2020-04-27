# Generated by Django 2.2.7 on 2020-04-27 08:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0027_auto_20200420_0223'),
        ('tags', '0003_auto_20200325_0246'),
        ('basket', '0025_auto_20200426_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='received',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 27, 11, 4, 36, 200435), verbose_name='received'),
        ),
        migrations.AddField(
            model_name='promocode',
            name='categories',
            field=models.ManyToManyField(related_name='promos', to='products.Category', verbose_name='categories'),
        ),
        migrations.AddField(
            model_name='promocode',
            name='products',
            field=models.ManyToManyField(help_text='At least 1 product is required.', related_name='promos', to='products.Product', verbose_name='products'),
        ),
        migrations.AddField(
            model_name='promocode',
            name='tags',
            field=models.ManyToManyField(help_text='At least 1 tag is required.', related_name='promos', to='tags.Tag', verbose_name='tags'),
        ),
    ]
