# Generated by Django 2.2.7 on 2020-03-22 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20200322_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_new',
            field=models.CharField(choices=[('new', 'New'), ('calculated', 'Calculated'), ('not_new', 'Not new')], default='calculated', max_length=12),
        ),
    ]
