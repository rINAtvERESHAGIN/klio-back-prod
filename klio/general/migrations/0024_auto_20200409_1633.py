# Generated by Django 2.2.7 on 2020-04-09 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0023_auto_20200406_0142'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='menu',
            unique_together={('name', 'position')},
        ),
    ]