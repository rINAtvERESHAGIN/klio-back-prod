# Generated by Django 2.2.7 on 2020-02-04 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0002_auto_20200204_0042'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='promocode',
            options={'ordering': ['-activity']},
        ),
    ]
