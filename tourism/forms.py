from django import forms
from .models import Reservation
from datetime import datetime, time, date, timedelta
from django.core.exceptions import ValidationError

def generate_12h_time_choices():
    choices = []
    start = datetime.combine(date.today(), datetime.strptime("05:00", "%H:%M").time())
    end = datetime.combine(date.today(), datetime.strptime("22:30", "%H:%M").time())
    current = start
    while current <= end:
        time_str_24h = current.strftime('%H:%M')
        time_str_12h = current.strftime('%I:%M %p').lstrip("0")
        choices.append((time_str_24h, time_str_12h))
        current += timedelta(minutes=30)
    return choices

class LimitedSpotReservationForm(forms.ModelForm):
    start_date = forms.ChoiceField(label="Start Date", widget=forms.Select())
    end_date = forms.ChoiceField(label="End Date", widget=forms.Select())
    time = forms.ChoiceField(choices=generate_12h_time_choices(), label="Time")
    note = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

    class Meta:
        model = Reservation
        fields = ['full_name', 'contact_number', 'num_guests', 'start_date', 'end_date', 'time', 'note']

    def __init__(self, *args, **kwargs):
        spot = kwargs.pop('spot', None)
        super().__init__(*args, **kwargs)

        if spot and spot.available_from and spot.available_until:
            date_choices = [
                (d.strftime('%Y-%m-%d'), d.strftime('%B %d, %Y'))
                for d in (spot.available_from + timedelta(days=i)
                          for i in range((spot.available_until - spot.available_from).days + 1))
            ]
            self.fields['start_date'].choices = date_choices
            self.fields['end_date'].choices = date_choices
        else:
            self.fields['start_date'].choices = []
            self.fields['end_date'].choices = []

    def clean(self):
        cleaned_data = super().clean()
        start_date_str = cleaned_data.get('start_date')
        end_date_str = cleaned_data.get('end_date')
        time_val = cleaned_data.get('time')

        if not start_date_str or not end_date_str or not time_val:
            raise forms.ValidationError("Start date, end date, and time are required.")

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        if start_date < date.today():
            raise forms.ValidationError("Start date cannot be in the past.")
        if end_date < start_date:
            raise forms.ValidationError("End date must be after the start date.")

        time_obj = datetime.strptime(time_val, '%H:%M').time()
        cleaned_data['reservation_datetime'] = datetime.combine(start_date, time_obj)
        cleaned_data['start_date'] = start_date
        cleaned_data['end_date'] = end_date
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.reservation_datetime = self.cleaned_data['reservation_datetime']
        instance.start_date = self.cleaned_data['start_date']
        instance.end_date = self.cleaned_data['end_date']
        if commit:
            instance.save()
        return instance


class UnlimitedSpotReservationForm(forms.ModelForm):
    start_date = forms.ChoiceField(label="Start Date", widget=forms.Select())
    end_date = forms.ChoiceField(label="End Date", widget=forms.Select())
    time = forms.ChoiceField(choices=generate_12h_time_choices(), label="Time")
    note = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

    class Meta:
        model = Reservation
        fields = ['full_name', 'contact_number', 'num_guests', 'start_date', 'end_date', 'time', 'note']

    def __init__(self, *args, **kwargs):
        spot = kwargs.pop('spot', None)
        super().__init__(*args, **kwargs)

        if spot and spot.available_from and spot.available_until:
            date_choices = [
                (d.strftime('%Y-%m-%d'), d.strftime('%B %d, %Y'))
                for d in (spot.available_from + timedelta(days=i)
                          for i in range((spot.available_until - spot.available_from).days + 1))
            ]
            self.fields['start_date'].choices = date_choices
            self.fields['end_date'].choices = date_choices
        else:
            self.fields['start_date'].choices = []
            self.fields['end_date'].choices = []

    def clean(self):
        cleaned_data = super().clean()
        start_date_str = cleaned_data.get('start_date')
        end_date_str = cleaned_data.get('end_date')
        time_val = cleaned_data.get('time')

        if not start_date_str or not end_date_str or not time_val:
            raise forms.ValidationError("Start date, end date, and time are required.")

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        if start_date < date.today():
            raise forms.ValidationError("Start date cannot be in the past.")
        if end_date < start_date:
            raise forms.ValidationError("End date must be after the start date.")

        time_obj = datetime.strptime(time_val, '%H:%M').time()
        cleaned_data['reservation_datetime'] = datetime.combine(start_date, time_obj)
        cleaned_data['start_date'] = start_date
        cleaned_data['end_date'] = end_date
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.reservation_datetime = self.cleaned_data['reservation_datetime']
        instance.start_date = self.cleaned_data['start_date']
        instance.end_date = self.cleaned_data['end_date']
        if commit:
            instance.save()
        return instance


class ReservationForm(forms.ModelForm):
    start_date = forms.ChoiceField(label="Start Date")
    end_date = forms.ChoiceField(label="End Date")
    time = forms.ChoiceField(choices=generate_12h_time_choices(), label="Time")

    class Meta:
        model = Reservation
        fields = ['full_name', 'contact_number', 'num_guests', 'start_date', 'end_date', 'time', 'note']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, tourist_spot=None, **kwargs):
        super().__init__(*args, **kwargs)

        if tourist_spot and tourist_spot.available_from and tourist_spot.available_until:
            # Generate dropdown choices for dates
            date_choices = [
                (d.strftime('%Y-%m-%d'), d.strftime('%B %d, %Y'))
                for d in (tourist_spot.available_from + timedelta(days=i)
                          for i in range((tourist_spot.available_until - tourist_spot.available_from).days + 1))
            ]
            self.fields['start_date'].choices = date_choices
            self.fields['end_date'].choices = date_choices

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        time_val = cleaned_data.get('time')

        if not start or not end or not time_val:
            raise forms.ValidationError('Start date, end date, and time are required.')

        start_date = datetime.strptime(start, '%Y-%m-%d').date()
        end_date = datetime.strptime(end, '%Y-%m-%d').date()
        if start_date > end_date:
            raise forms.ValidationError('Start date must be before or equal to end date.')

        # You can store parsed dates if needed
        cleaned_data['start_date'] = start_date
        cleaned_data['end_date'] = end_date
        return cleaned_data