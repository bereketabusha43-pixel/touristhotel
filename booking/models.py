"""
Booking models: guests and reservations.
"""
import uuid

from django.db import models
from django.urls import reverse
from django.utils import timezone

from core.mixins import TimeStampedModel
from rooms.models import Room


class Guest(TimeStampedModel):
    """Guest information for bookings."""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    country = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    passport_number = models.CharField(max_length=50, blank=True)
    special_requests = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Booking(TimeStampedModel):
    """Room reservation."""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    PAYMENT_STATUS = [
        ('unpaid', 'Unpaid'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]

    reference = models.CharField(max_length=20, unique=True, editable=False)
    guest = models.ForeignKey(Guest, on_delete=models.PROTECT, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    adults = models.PositiveSmallIntegerField(default=1)
    children = models.PositiveSmallIntegerField(default=0)
    num_rooms = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='unpaid')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    special_requests = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.reference} — {self.guest.full_name}'

    def save(self, *args, **kwargs):
        if not self.reference:
            from django.conf import settings
            prefix = getattr(settings, 'BOOKING_REFERENCE_PREFIX', 'AMTH')
            self.reference = f'{prefix}-{uuid.uuid4().hex[:8].upper()}'
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse('booking:confirmation', kwargs={'reference': self.reference})

    @property
    def nights(self) -> int:
        return (self.check_out - self.check_in).days

    @property
    def is_active(self) -> bool:
        return self.status in ('pending', 'confirmed', 'checked_in')

    def confirm(self) -> None:
        self.status = 'confirmed'
        self.confirmed_at = timezone.now()
        self.save(update_fields=['status', 'confirmed_at', 'updated_at'])
