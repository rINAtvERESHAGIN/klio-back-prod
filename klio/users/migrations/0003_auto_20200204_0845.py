# Generated by Django 2.2.7 on 2020-02-04 08:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_auto_20200204_0845'),
        ('users', '0002_auto_20200203_2348'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-activity', 'last_name', 'username']},
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
        migrations.CreateModel(
            name='UserPhone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main', models.BooleanField(default=False)),
                ('order', models.PositiveSmallIntegerField(default=1)),
                ('activity', models.BooleanField(default=True)),
                ('phone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contacts.Phone')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='phones',
            field=models.ManyToManyField(related_name='users', through='users.UserPhone', to='contacts.Phone'),
        ),
    ]
