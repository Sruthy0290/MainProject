# Generated by Django 4.2.4 on 2024-03-14 04:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0058_order_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='quantity',
        ),
    ]
