# Generated by Django 2.2.7 on 2020-06-17 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0048_category_with_general_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, help_text='Choose the most detailed categories', related_name='products', to='products.Category', verbose_name='categories'),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
    ]
