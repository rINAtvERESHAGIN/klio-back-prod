# Generated by Django 2.2.7 on 2020-03-21 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20200321_1645'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brand',
            options={'ordering': ['-activity', 'order'], 'verbose_name': 'Brand', 'verbose_name_plural': 'Brands'},
        ),
        migrations.AddField(
            model_name='product',
            name='base_ammount',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='units',
            field=models.CharField(blank=True, max_length=32, verbose_name='Units'),
        ),
        migrations.AlterField(
            model_name='productproperty',
            name='units',
            field=models.CharField(blank=True, max_length=32, verbose_name='Units'),
        ),
    ]
