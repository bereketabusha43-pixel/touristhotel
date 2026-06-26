"""Blog search form."""
from django import forms

from blog.models import BlogCategory


class BlogSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search articles...'}),
    )
    category = forms.ModelChoiceField(
        queryset=BlogCategory.objects.filter(is_published=True),
        required=False,
        empty_label='All Categories',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
