# Generated by Django 2.2.7 on 2020-05-19 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0040_auto_20200505_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='img',
            field=models.ImageField(blank=True, upload_to='categories', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='label',
            field=models.CharField(blank=True, max_length=128, verbose_name='label'),
        ),
    ]