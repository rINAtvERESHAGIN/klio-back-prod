# Generated by Django 2.2.7 on 2020-03-22 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_product_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productimage',
            options={'ordering': ['-activity', 'order'], 'verbose_name': 'Product image', 'verbose_name_plural': 'Product images'},
        ),
        migrations.AddField(
            model_name='product',
            name='is_new',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.Product'),
        ),
    ]
