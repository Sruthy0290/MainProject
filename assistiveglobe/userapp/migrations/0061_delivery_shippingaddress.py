# Generated by Django 4.2.4 on 2024-03-15 05:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0060_delivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='shippingaddress',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userapp.shippingaddress'),
        ),
    ]