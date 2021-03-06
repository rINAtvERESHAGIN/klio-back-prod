# Generated by Django 2.2.7 on 2020-04-28 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0026_auto_20200423_0839'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='meta_description',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='meta description'),
        ),
        migrations.AddField(
            model_name='article',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='meta keywords'),
        ),
        migrations.AddField(
            model_name='article',
            name='meta_title',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='meta title'),
        ),
        migrations.AddField(
            model_name='news',
            name='meta_description',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='meta description'),
        ),
        migrations.AddField(
            model_name='news',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='meta keywords'),
        ),
        migrations.AddField(
            model_name='news',
            name='meta_title',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='meta title'),
        ),
        migrations.AddField(
            model_name='page',
            name='meta_description',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='meta description'),
        ),
        migrations.AddField(
            model_name='page',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='meta keywords'),
        ),
        migrations.AddField(
            model_name='page',
            name='meta_title',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='meta title'),
        ),
    ]
