# Generated by Django 4.2.4 on 2023-09-18 04:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0016_customuser_last_logged_in'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='last_logged_in',
        ),
    ]
