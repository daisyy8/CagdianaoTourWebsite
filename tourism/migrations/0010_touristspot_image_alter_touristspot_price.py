# Generated by Django 5.2.1 on 2025-05-25 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourism', '0009_touristspot_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='touristspot',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='tourist_spot_images/'),
        ),
        migrations.AlterField(
            model_name='touristspot',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
            preserve_default=False,
        ),
    ]
