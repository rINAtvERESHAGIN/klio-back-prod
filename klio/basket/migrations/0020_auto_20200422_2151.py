# Generated by Django 2.2.7 on 2020-04-22 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0019_auto_20200422_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderprivateinfo',
            name='middle_name',
            field=models.CharField(blank=True, default=None, max_length=128, null=True, verbose_name='middle name'),
        ),
    ]
