# Generated by Django 4.2.4 on 2024-02-15 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0044_remove_appointment_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='cancelled',
            field=models.BooleanField(default=False),
        ),
    ]
