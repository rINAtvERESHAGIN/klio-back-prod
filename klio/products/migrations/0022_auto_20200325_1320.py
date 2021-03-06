# Generated by Django 2.2.7 on 2020-03-25 10:20

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_auto_20200324_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='activity',
            field=models.BooleanField(default=True, verbose_name='activity'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='logo',
            field=models.ImageField(upload_to='', verbose_name='logo'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=64, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='order',
            field=models.PositiveIntegerField(default=1, verbose_name='order'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='slug',
            field=models.SlugField(verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='category',
            name='activity',
            field=models.BooleanField(default=True, verbose_name='activity'),
        ),
        migrations.AlterField(
            model_name='category',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='category',
            name='group',
            field=models.PositiveIntegerField(default=0, editable=False, null=True, verbose_name='group'),
        ),
        migrations.AlterField(
            model_name='category',
            name='img',
            field=models.ImageField(upload_to='', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='category',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=64, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='on_main',
            field=models.BooleanField(default=False, verbose_name='on main'),
        ),
        migrations.AlterField(
            model_name='category',
            name='order',
            field=models.PositiveIntegerField(default=1, verbose_name='order'),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='products.Category', verbose_name='parent'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='categorycityrating',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Category', verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='categorycityrating',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cities_light.City', verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='categorycityrating',
            name='rating',
            field=models.PositiveIntegerField(default=0, null=True, verbose_name='rating'),
        ),
        migrations.AlterField(
            model_name='product',
            name='activity',
            field=models.BooleanField(default=True, verbose_name='activity'),
        ),
        migrations.AlterField(
            model_name='product',
            name='art',
            field=models.IntegerField(blank=True, null=True, verbose_name='vendor code'),
        ),
        migrations.AlterField(
            model_name='product',
            name='base_amount',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, verbose_name='base amount'),
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Brand', verbose_name='brand'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Category', verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_new',
            field=models.CharField(choices=[('new', 'New'), ('calculated', 'Calculated'), ('not_new', 'Not new')], default='calculated', max_length=12, verbose_name='is new'),
        ),
        migrations.AlterField(
            model_name='product',
            name='kind',
            field=models.CharField(choices=[('unique', 'Unique product'), ('parent', 'Child product'), ('child', 'Parent product')], max_length=7, verbose_name='kind'),
        ),
        migrations.AlterField(
            model_name='product',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=64, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='order',
            field=models.PositiveIntegerField(default=1, verbose_name='order'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='products.ProductType', verbose_name='product type'),
        ),
        migrations.AlterField(
            model_name='product',
            name='properties',
            field=models.ManyToManyField(related_name='products', through='products.ProductPropertyValue', to='products.ProductProperty', verbose_name='properties'),
        ),
        migrations.AlterField(
            model_name='product',
            name='recommended',
            field=models.ManyToManyField(blank=True, related_name='_product_recommended_+', to='products.Product', verbose_name='recommended'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='products', to='tags.Tag', verbose_name='tags'),
        ),
        migrations.AlterField(
            model_name='product',
            name='units',
            field=models.CharField(blank=True, max_length=32, verbose_name='units'),
        ),
        migrations.AlterField(
            model_name='product',
            name='wholesale_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='wholesale price'),
        ),
        migrations.AlterField(
            model_name='product',
            name='wholesale_threshold',
            field=models.IntegerField(blank=True, null=True, verbose_name='wholesale threshold'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='activity',
            field=models.BooleanField(default=True, verbose_name='activity'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='img',
            field=models.ImageField(upload_to='', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='label',
            field=models.CharField(blank=True, max_length=64, verbose_name='label'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='order',
            field=models.PositiveIntegerField(default=1, verbose_name='order'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.Product', verbose_name='product'),
        ),
        migrations.AlterField(
            model_name='productproperty',
            name='name',
            field=models.CharField(max_length=128, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='productproperty',
            name='required',
            field=models.BooleanField(default=False, verbose_name='required'),
        ),
        migrations.AlterField(
            model_name='productproperty',
            name='type',
            field=models.CharField(choices=[('text', 'Text'), ('integer', 'Integer'), ('boolean', 'True / False'), ('float', 'Float'), ('richtext', 'Rich Text'), ('date', 'Date'), ('datetime', 'Datetime')], default='text', max_length=20, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='productproperty',
            name='units',
            field=models.CharField(blank=True, max_length=32, verbose_name='units'),
        ),
        migrations.AlterField(
            model_name='productpropertyvalue',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_values', to='products.Product', verbose_name='product'),
        ),
        migrations.AlterField(
            model_name='productpropertyvalue',
            name='prop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='products.ProductProperty', verbose_name='property'),
        ),
        migrations.AlterField(
            model_name='productpropertyvalue',
            name='value_file',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to='products/properties/files', verbose_name='file'),
        ),
        migrations.AlterField(
            model_name='productpropertyvalue',
            name='value_image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='products/properties/images', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='activity',
            field=models.BooleanField(default=True, verbose_name='activity'),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Category', verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='name',
            field=models.CharField(max_length=64, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='slug',
            field=models.SlugField(verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='userproduct',
            name='added',
            field=models.DateTimeField(auto_now_add=True, verbose_name='added'),
        ),
        migrations.AlterField(
            model_name='userproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product', verbose_name='product'),
        ),
        migrations.AlterField(
            model_name='userproduct',
            name='selected',
            field=models.BooleanField(default=False, verbose_name='selected'),
        ),
        migrations.AlterField(
            model_name='userproduct',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
