# Generated by Django 2.2.7 on 2020-03-19 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0008_auto_20200319_1104'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='socialnet',
            options={'ordering': ['-activity', 'order', 'name']},
        ),
        migrations.AddField(
            model_name='socialnet',
            name='order',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
