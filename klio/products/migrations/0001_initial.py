# Generated by Django 2.2.7 on 2020-02-03 23:31

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64)),
                ('slug', models.SlugField()),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('activity', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64)),
                ('slug', models.SlugField()),
                ('img', models.ImageField(upload_to='')),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('activity', models.BooleanField(default=True)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64)),
                ('slug', models.SlugField()),
                ('description', ckeditor.fields.RichTextField()),
                ('kind', models.CharField(choices=[('unique', 'Unique product'), ('parent', 'Child product'), ('child', 'Parent product')], max_length=7)),
                ('art', models.IntegerField()),
                ('in_stock', models.DecimalField(decimal_places=4, max_digits=10, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('wholesale_threshold', models.IntegerField(blank=True)),
                ('wholesale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('order', models.PositiveIntegerField(default=1)),
                ('activity', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductAttr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=1)),
                ('activity', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('type', models.CharField(choices=[('text', 'Text'), ('integer', 'Integer'), ('boolean', 'True / False'), ('float', 'Float'), ('richtext', 'Rich Text'), ('date', 'Date'), ('datetime', 'Datetime')], default='text', max_length=20, verbose_name='Type')),
                ('units', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='UserProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('selected', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64)),
                ('slug', models.SlugField()),
                ('activity', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=64)),
                ('order', models.PositiveIntegerField(default=1)),
                ('activity', models.BooleanField(default=True)),
                ('value_text', models.TextField(blank=True, null=True, verbose_name='Text')),
                ('value_integer', models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Integer')),
                ('value_boolean', models.NullBooleanField(db_index=True, verbose_name='Boolean')),
                ('value_float', models.FloatField(blank=True, db_index=True, null=True, verbose_name='Float')),
                ('value_richtext', models.TextField(blank=True, null=True, verbose_name='Richtext')),
                ('value_date', models.DateField(blank=True, db_index=True, null=True, verbose_name='Date')),
                ('value_datetime', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='DateTime')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Property')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='')),
                ('label', models.CharField(blank=True, max_length=64)),
                ('order', models.PositiveIntegerField(default=1)),
                ('activity', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductAttrValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=64)),
                ('attr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.ProductAttr')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
        migrations.AddField(
            model_name='productattr',
            name='product_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.ProductType'),
        ),
        migrations.AddField(
            model_name='productattr',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Property'),
        ),
        migrations.AddField(
            model_name='product',
            name='attr',
            field=models.ManyToManyField(through='products.ProductAttrValue', to='products.ProductAttr'),
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Brand'),
        ),
        migrations.AddField(
            model_name='product',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Product'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.ProductType'),
        ),
        migrations.AddField(
            model_name='product',
            name='property',
            field=models.ManyToManyField(through='products.ProductProperty', to='products.Property'),
        ),
    ]
