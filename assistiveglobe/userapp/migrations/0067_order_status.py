# Generated by Django 4.2.4 on 2024-03-22 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0066_remove_orderitem_accepted_by_delivery_person_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='Pending', max_length=50),
        ),
    ]