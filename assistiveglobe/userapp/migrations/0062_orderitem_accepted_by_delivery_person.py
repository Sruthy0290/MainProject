# Generated by Django 4.2.4 on 2024-03-15 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0061_delivery_shippingaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='accepted_by_delivery_person',
            field=models.BooleanField(default=False),
        ),
    ]
