# Generated by Django 4.2.1 on 2023-08-09 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='number',
        ),
    ]
