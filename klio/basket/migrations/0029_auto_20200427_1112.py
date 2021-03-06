# Generated by Django 2.2.7 on 2020-04-27 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0028_auto_20200427_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocode',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='promos', to='products.Category', verbose_name='categories'),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='promos', to='products.Product', verbose_name='products'),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='promos', to='tags.Tag', verbose_name='tags'),
        ),
    ]
