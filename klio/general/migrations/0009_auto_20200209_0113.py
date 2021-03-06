# Generated by Django 2.2.7 on 2020-02-08 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0008_auto_20200208_1443'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='page',
            options={'ordering': ['-activity', 'name'], 'verbose_name': 'Page', 'verbose_name_plural': 'Pages'},
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='general.Menu'),
        ),
    ]
