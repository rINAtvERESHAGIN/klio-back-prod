# Generated by Django 2.2.7 on 2020-03-18 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0004_contact_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkingHours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=32)),
                ('time', models.CharField(max_length=32)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contacts.Contact')),
            ],
        ),
    ]
