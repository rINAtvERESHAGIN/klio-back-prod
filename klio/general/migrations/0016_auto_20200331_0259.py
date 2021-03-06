# Generated by Django 2.2.7 on 2020-03-30 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0015_auto_20200325_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='abstract',
            field=models.TextField(default=1, help_text='Short description - 256 symbols max.', max_length=256, verbose_name='abstract'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='news',
            name='abstract',
            field=models.TextField(default=1, help_text='Short description - 256 symbols max.', max_length=256, verbose_name='abstract'),
            preserve_default=False,
        ),
    ]
