# Generated by Django 2.2.7 on 2020-04-27 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0033_auto_20200427_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('active', 'Order is active'), ('pending', 'Order pending'), ('delivery', 'Order on delivery'), ('completed', 'Order completed'), ('denied', 'Order denied')], default='active', max_length=10, verbose_name='status'),
        ),
    ]
