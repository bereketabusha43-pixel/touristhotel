"""Room search and filter forms."""
from django import forms

from rooms.models import Room, RoomCategory


class RoomSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search rooms...'}),
    )
    category = forms.ModelChoiceField(
        queryset=RoomCategory.objects.all(),
        required=False,
        empty_label='All Categories',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    min_price = forms.DecimalField(
        required=False, min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min Price'}),
    )
    max_price = forms.DecimalField(
        required=False, min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max Price'}),
    )
    bed_type = forms.ChoiceField(
        choices=[('', 'All Bed Types')] + list(Room.BED_TYPES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    lake_view = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
