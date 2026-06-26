"""Booking forms."""
from datetime import date

from django import forms

from booking.models import Booking, Guest
from booking.services import BookingService
from rooms.models import Room


class AvailabilitySearchForm(forms.Form):
    """Quick availability search widget form."""

    check_in = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Check-in',
    )
    check_out = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Check-out',
    )
    adults = forms.IntegerField(
        min_value=1, max_value=10, initial=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
    )
    children = forms.IntegerField(
        min_value=0, max_value=10, initial=0, required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
    )
    num_rooms = forms.IntegerField(
        min_value=1, max_value=5, initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
    )

    def clean(self):
        cleaned = super().clean()
        check_in = cleaned.get('check_in')
        check_out = cleaned.get('check_out')
        if check_in and check_out:
            if check_in < date.today():
                raise forms.ValidationError('Check-in date cannot be in the past.')
            if check_out <= check_in:
                raise forms.ValidationError('Check-out must be after check-in.')
        return cleaned


class BookingForm(forms.ModelForm):
    """Full booking reservation form."""

    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Booking
        fields = ['check_in', 'check_out', 'adults', 'children', 'num_rooms', 'special_requests']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'adults': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'children': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'num_rooms': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, room: Room | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = room

    def clean(self):
        cleaned = super().clean()
        check_in = cleaned.get('check_in')
        check_out = cleaned.get('check_out')
        if self.room and check_in and check_out:
            if not BookingService.is_room_available(self.room, check_in, check_out):
                raise forms.ValidationError('This room is not available for the selected dates.')
        return cleaned

    def save(self, commit=True) -> Booking:
        guest = Guest.objects.create(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            phone=self.cleaned_data['phone'],
            country=self.cleaned_data.get('country', ''),
            special_requests=self.cleaned_data.get('special_requests', ''),
        )
        booking = super().save(commit=False)
        booking.guest = guest
        booking.room = self.room
        if self.room:
            booking.total_price = BookingService.calculate_total(
                self.room, booking.check_in, booking.check_out, booking.num_rooms
            )
        if commit:
            booking.save()
        return booking
