"""Conference and event inquiry forms."""
from django import forms

from conference.models import ConferenceBooking, ConferenceHall, EventInquiry


class ConferenceBookingForm(forms.ModelForm):
    hall = forms.ModelChoiceField(
        queryset=ConferenceHall.objects.filter(is_published=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = ConferenceBooking
        fields = [
            'hall', 'organization', 'contact_name', 'email', 'phone',
            'event_date', 'start_time', 'end_time', 'attendees', 'event_type', 'requirements',
        ]
        widgets = {
            'organization': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'event_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'attendees': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'event_type': forms.TextInput(attrs={'class': 'form-control'}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class EventInquiryForm(forms.ModelForm):
    class Meta:
        model = EventInquiry
        fields = ['name', 'email', 'phone', 'event_date', 'guests', 'event_type', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'event_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'event_type': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
