from django.contrib import admin
from django import forms
from django.forms.widgets import MultiWidget, Select
from datetime import time
from .models import TouristSpot, Profile, Reservation

admin.site.register(Profile)
admin.site.register(Reservation)

class Time12HourWidget(MultiWidget):
    def __init__(self, attrs=None):
        hours = [(str(i), f'{i}') for i in range(1, 13)]
        minutes = [(f'{i:02}', f'{i:02}') for i in range(0, 60, 5)]  # 5-minute steps
        am_pm = [('AM', 'AM'), ('PM', 'PM')]
        widgets = [
            Select(attrs=attrs, choices=hours),
            Select(attrs=attrs, choices=minutes),
            Select(attrs=attrs, choices=am_pm),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            hour = value.hour
            minute = value.minute
            meridian = 'AM'
            if hour == 0:
                hour = 12
                meridian = 'AM'
            elif hour == 12:
                meridian = 'PM'
            elif hour > 12:
                hour -= 12
                meridian = 'PM'
            return [str(hour), f'{minute:02}', meridian]
        return [None, None, None]

    def format_output(self, rendered_widgets):
        return ':'.join(rendered_widgets[:2]) + ' ' + rendered_widgets[2]

    def value_from_datadict(self, data, files, name):
        hour = int(data.get(f'{name}_0', 0))
        minute = int(data.get(f'{name}_1', 0))
        meridian = data.get(f'{name}_2', 'AM')
        if meridian == 'PM' and hour != 12:
            hour += 12
        elif meridian == 'AM' and hour == 12:
            hour = 0
        return time(hour, minute)

class TouristSpotAdminForm(forms.ModelForm):
    class Meta:
        model = TouristSpot
        fields = '__all__'
        widgets = {
            'time_open': Time12HourWidget(),
            'time_closed': Time12HourWidget(),
        }

@admin.register(TouristSpot)
class TouristSpotAdmin(admin.ModelAdmin):
    form = TouristSpotAdminForm
    list_display = ('name', 'location', 'is_limited', 'price', 'cottage_price', 'available_from', 'available_until')
    list_editable = ('is_limited', 'price', 'cottage_price', 'available_from', 'available_until')
