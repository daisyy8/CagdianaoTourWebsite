# Generated by Django 5.2.1 on 2025-05-22 02:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tourism', '0006_reservation_price_touristspot_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='price',
        ),
    ]
