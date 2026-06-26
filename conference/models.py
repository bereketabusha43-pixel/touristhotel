"""
Conference and events models.
"""
from django.db import models
from django.urls import reverse

from core.mixins import PublishableModel, SEOModel, TimeStampedModel, unique_slugify


class ConferenceHall(PublishableModel, SEOModel, TimeStampedModel):
    """Meeting rooms and conference halls."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    capacity = models.PositiveIntegerField(help_text='Maximum seating capacity')
    size_sqm = models.PositiveIntegerField(help_text='Hall size in square meters')
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_half_day = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    equipment = models.TextField(blank=True, help_text='One item per line')
    main_image = models.ImageField(upload_to='conference/', blank=True)
    floor = models.PositiveSmallIntegerField(default=1)
    has_natural_light = models.BooleanField(default=True)
    has_stage = models.BooleanField(default=False)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse('conference:detail', kwargs={'slug': self.slug})

    def get_equipment_list(self) -> list[str]:
        return [line.strip() for line in self.equipment.splitlines() if line.strip()]


class ConferenceBooking(TimeStampedModel):
    """Conference hall booking inquiry."""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    hall = models.ForeignKey(ConferenceHall, on_delete=models.PROTECT, related_name='bookings')
    organization = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    attendees = models.PositiveIntegerField()
    event_type = models.CharField(max_length=100, blank=True)
    requirements = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['-event_date']

    def __str__(self) -> str:
        return f'{self.organization} — {self.hall.name}'


class EventPackage(PublishableModel, SEOModel, TimeStampedModel):
    """Wedding, graduation, and event packages."""

    EVENT_TYPES = [
        ('wedding', 'Wedding'),
        ('graduation', 'Graduation'),
        ('birthday', 'Birthday'),
        ('corporate', 'Corporate Event'),
        ('outdoor', 'Outdoor Event'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_guests = models.PositiveIntegerField(default=100)
    includes = models.TextField(blank=True, help_text='One item per line')
    image = models.ImageField(upload_to='events/', blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse('conference:event_detail', kwargs={'slug': self.slug})

    def get_includes_list(self) -> list[str]:
        return [line.strip() for line in self.includes.splitlines() if line.strip()]


class EventInquiry(TimeStampedModel):
    """Event package inquiry form submissions."""

    package = models.ForeignKey(
        EventPackage, on_delete=models.SET_NULL, null=True, blank=True, related_name='inquiries'
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    event_date = models.DateField()
    guests = models.PositiveIntegerField()
    event_type = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Event Inquiries'

    def __str__(self) -> str:
        return f'{self.name} — {self.event_type}'
