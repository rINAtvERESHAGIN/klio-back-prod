# Generated by Django 2.2.7 on 2020-04-30 01:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0032_auto_20200430_0332'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productpropertyvalue',
            old_name='property',
            new_name='prop',
        ),
        migrations.AlterField(
            model_name='product',
            name='art',
            field=models.IntegerField(blank=True, help_text='Do not set article number for parent product.', null=True, verbose_name='vendor code'),
        ),
        migrations.AlterField(
            model_name='product',
            name='base_amount',
            field=models.DecimalField(blank=True, decimal_places=4, help_text='Used for correct displaying and calculating the amount and the price of a product.', max_digits=10, null=True, verbose_name='base amount'),
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, help_text='If this field is empty for child product, Brand will be inherited fromparent.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Brand', verbose_name='brand'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, help_text='Choose the most detailed category', null=True, on_delete=django.db.models.deletion.PROTECT, to='products.Category', verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_new',
            field=models.CharField(choices=[('new', 'New'), ('calculated', 'Calculated'), ('not_new', 'Not new')], default='calculated', help_text="If set to 'Calculated', the product will be valued as new for 2 months fromthe date of adding", max_length=12, verbose_name='is new'),
        ),
        migrations.AlterField(
            model_name='product',
            name='parent',
            field=models.ForeignKey(blank=True, help_text='Leave blank if this is a unique product', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='products.Product', verbose_name='Parent product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Do not set the price on a parent product.', max_digits=10, null=True, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.ForeignKey(blank=True, help_text="Choose the product type. Properties will be inherited after saving.Click 'Save & Continue' button.", null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='products.ProductType', verbose_name='product type'),
        ),
        migrations.AlterField(
            model_name='product',
            name='properties',
            field=models.ManyToManyField(help_text='Properties should be set on Product Type level, but you canprovide single-product property as well.', related_name='products', through='products.ProductPropertyValue', to='products.ProductProperty', verbose_name='properties'),
        ),
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, help_text='If not provided for child product, tags will be inherited from parent.', related_name='products', to='tags.Tag', verbose_name='tags'),
        ),
        migrations.AlterUniqueTogether(
            name='productpropertyvalue',
            unique_together={('prop', 'product')},
        ),
    ]
