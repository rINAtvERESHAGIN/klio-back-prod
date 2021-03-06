# Generated by Django 2.2.7 on 2020-01-27 12:10

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities_light', '0008_city_timezone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64)),
                ('address', models.CharField(max_length=256)),
                ('email', models.EmailField(max_length=254)),
                ('map', models.URLField(blank=True)),
                ('content', ckeditor.fields.RichTextField(blank=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cities_light.City')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cities_light.Country')),
            ],
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(default=None, help_text='Enter the phone in the format +7(XXX)XXX-XX-XX', max_length=20)),
                ('label', models.CharField(blank=True, default=None, max_length=64)),
                ('activity', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='SocialNet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='ContactPhone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main', models.BooleanField(default=False)),
                ('order', models.PositiveSmallIntegerField(default=1)),
                ('activity', models.BooleanField(default=True)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contacts.Contact')),
                ('phone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contacts.Phone')),
            ],
        ),
        migrations.AddField(
            model_name='contact',
            name='phones',
            field=models.ManyToManyField(through='contacts.ContactPhone', to='contacts.Phone'),
        ),
    ]
