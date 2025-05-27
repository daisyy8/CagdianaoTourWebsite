#Models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from datetime import date

def default_open_time():
    return datetime.time(8, 0)

def default_close_time():
    return datetime.time(17, 0) 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class TouristSpot(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cottage_price = models.DecimalField(max_digits=6, decimal_places=2)
    available_from = models.DateField(default=date.today)
    available_until = models.DateField(default=date.today)
    is_limited = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Set a number limit for bookings per day (leave blank for unlimited)"
    )
    image = models.ImageField(upload_to='tourist_spot_images/', default='default.jpg')
    time_open = models.TimeField(default=default_open_time)
    time_closed = models.TimeField(default=default_close_time)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spot = models.ForeignKey(
        TouristSpot,
        on_delete=models.CASCADE,
        related_name='reservations' 
    )
    full_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    num_guests = models.PositiveIntegerField(default=1)
    reservation_datetime = models.DateTimeField(default=timezone.now)
    note = models.TextField(blank=True, null=True)
    cottage_number = models.PositiveIntegerField(blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    is_accepted = models.BooleanField(default=False)
    


    def save(self, *args, **kwargs):
        if self.spot.is_limited:
            existing_reservations = Reservation.objects.filter(
                spot=self.spot,
                reservation_datetime__date=self.reservation_datetime.date()
            )
            if self.pk is None and existing_reservations.count() >= 5:
                raise ValueError("This day is fully booked.")
            if self.cottage_number is None:
                self.cottage_number = existing_reservations.count() + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reservation for {self.full_name} on {self.reservation_datetime.strftime('%Y-%m-%d %H:%M')}"


