# Generated by Django 4.2.4 on 2024-03-04 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0055_alter_orderitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
