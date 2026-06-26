"""Contact and newsletter forms."""
from django import forms

from contact.models import ContactMessage, NewsletterSubscriber


class ContactForm(forms.ModelForm):
  class Meta:
    model = ContactMessage
    fields = ['name', 'email', 'phone', 'subject', 'message']
    widgets = {
      'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
      'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
      'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
      'subject': forms.Select(attrs={'class': 'form-select'}),
      'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your Message'}),
    }


class NewsletterForm(forms.ModelForm):
  class Meta:
    model = NewsletterSubscriber
    fields = ['email']
    widgets = {
      'email': forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email address',
        'aria-label': 'Email for newsletter',
      }),
    }

  def clean_email(self):
    email = self.cleaned_data['email'].lower()
    if NewsletterSubscriber.objects.filter(email=email, is_active=True).exists():
      raise forms.ValidationError('This email is already subscribed.')
    return email
