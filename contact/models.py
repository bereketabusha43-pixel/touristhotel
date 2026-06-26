"""
Contact models for messages and newsletter subscriptions.
"""
from django.db import models

from core.mixins import TimeStampedModel


class ContactMessage(TimeStampedModel):
    """Contact form submissions."""

    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('booking', 'Booking Question'),
        ('conference', 'Conference & Events'),
        ('feedback', 'Feedback'),
        ('complaint', 'Complaint'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='general')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    is_replied = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.name} — {self.get_subject_display()}'


class NewsletterSubscriber(TimeStampedModel):
    """Newsletter email subscriptions."""

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    confirmed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.email
