# Generated by Django 2.2.7 on 2020-02-05 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductPropertyValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_text', models.TextField(blank=True, null=True, verbose_name='Text')),
                ('value_integer', models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Integer')),
                ('value_boolean', models.NullBooleanField(db_index=True, verbose_name='Boolean')),
                ('value_float', models.FloatField(blank=True, db_index=True, null=True, verbose_name='Float')),
                ('value_richtext', models.TextField(blank=True, null=True, verbose_name='Richtext')),
                ('value_date', models.DateField(blank=True, db_index=True, null=True, verbose_name='Date')),
                ('value_datetime', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='DateTime')),
                ('value_file', models.FileField(blank=True, max_length=255, null=True, upload_to='products/properties/files')),
                ('value_image', models.ImageField(blank=True, max_length=255, null=True, upload_to='products/properties/images')),
            ],
            options={
                'verbose_name': 'Product property value',
                'verbose_name_plural': 'Product property values',
            },
        ),
        migrations.RemoveField(
            model_name='productattrvalue',
            name='attr',
        ),
        migrations.RemoveField(
            model_name='productattrvalue',
            name='product',
        ),
        migrations.AlterModelOptions(
            name='brand',
            options={'ordering': ['-activity'], 'verbose_name': 'Brand', 'verbose_name_plural': 'Brands'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-activity'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-activity', 'product_type', 'order'], 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AlterModelOptions(
            name='productimage',
            options={'ordering': ['-activity'], 'verbose_name': 'Product image', 'verbose_name_plural': 'Product images'},
        ),
        migrations.AlterModelOptions(
            name='productproperty',
            options={'verbose_name': 'Property', 'verbose_name_plural': 'Properties'},
        ),
        migrations.AlterModelOptions(
            name='producttype',
            options={'ordering': ['-activity', 'category', 'name'], 'verbose_name': 'Product type', 'verbose_name_plural': 'Product types'},
        ),
        migrations.RemoveField(
            model_name='product',
            name='attr',
        ),
        migrations.RemoveField(
            model_name='productproperty',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='productproperty',
            name='order',
        ),
        migrations.RemoveField(
            model_name='productproperty',
            name='product',
        ),
        migrations.RemoveField(
            model_name='productproperty',
            name='property',
        ),
        migrations.RemoveField(
            model_name='productproperty',
            name='value',
        ),
        migrations.RemoveField(
            model_name='productproperty',
            name='value_boolean',
        ),
        migrations.RemoveField(
            model_name='productproperty',
            name='value_date',
        ),
        migrations.RemoveField(
            model_name='productproperty',
            name='value_datetime',
        ),
        migrations.RemoveField(
            model_name='productproperty',
            name='value_float',
        ),
        migrations.RemoveField(
            model_name='productproperty',
            name='value_integer',
        ),
        migrations.RemoveField(
            model_name='productproperty',
            name='value_richtext',
        ),
        migrations.RemoveField(
            model_name='productproperty',
            name='value_text',
        ),
        migrations.AddField(
            model_name='productproperty',
            name='name',
            field=models.CharField(default=1, max_length=128, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productproperty',
            name='required',
            field=models.BooleanField(default=False, verbose_name='Required'),
        ),
        migrations.AddField(
            model_name='productproperty',
            name='type',
            field=models.CharField(choices=[('text', 'Text'), ('integer', 'Integer'), ('boolean', 'True / False'), ('float', 'Float'), ('richtext', 'Rich Text'), ('date', 'Date'), ('datetime', 'Datetime')], default='text', max_length=20, verbose_name='Type'),
        ),
        migrations.AddField(
            model_name='productproperty',
            name='units',
            field=models.CharField(blank=True, max_length=64, verbose_name='Units'),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='art',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='in_stock',
            field=models.DecimalField(blank=True, decimal_places=4, help_text='For parents it will be calculated automatically', max_digits=10, null=True, verbose_name='In_stock'),
        ),
        migrations.AlterField(
            model_name='product',
            name='parent',
            field=models.ForeignKey(blank=True, help_text='Leave blank if this is a unique product (i.e. product does not have children)', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='products.Product', verbose_name='Parent product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='products.ProductType'),
        ),
        migrations.AlterField(
            model_name='product',
            name='property',
            field=models.ManyToManyField(through='products.ProductPropertyValue', to='products.ProductProperty'),
        ),
        migrations.DeleteModel(
            name='ProductAttr',
        ),
        migrations.DeleteModel(
            name='ProductAttrValue',
        ),
        migrations.DeleteModel(
            name='Property',
        ),
        migrations.AddField(
            model_name='productpropertyvalue',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_values', to='products.Product', verbose_name='Product'),
        ),
        migrations.AddField(
            model_name='productpropertyvalue',
            name='prop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.ProductProperty', verbose_name='Property'),
        ),
        migrations.AlterUniqueTogether(
            name='productpropertyvalue',
            unique_together={('prop', 'product')},
        ),
    ]
