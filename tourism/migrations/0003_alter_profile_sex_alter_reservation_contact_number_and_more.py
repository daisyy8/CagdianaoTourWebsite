# Generated by Django 5.2.1 on 2025-05-20 14:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourism', '0002_rename_special_requests_reservation_note_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='contact_number',
            field=models.CharField(default='#', max_length=15),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='full_name',
            field=models.CharField(default='Contact Person', max_length=100),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reservation_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
