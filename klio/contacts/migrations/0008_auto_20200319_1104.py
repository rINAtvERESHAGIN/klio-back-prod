# Generated by Django 2.2.7 on 2020-03-19 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0007_auto_20200319_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialnet',
            name='img',
            field=models.FileField(upload_to='socials/'),
        ),
    ]
