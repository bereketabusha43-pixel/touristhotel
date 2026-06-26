"""
Room models: categories, rooms, images, and amenities.
"""
from django.db import models
from django.urls import reverse

from core.mixins import PublishableModel, SEOModel, TimeStampedModel, unique_slugify


class RoomCategory(TimeStampedModel):
    """Room type categories."""

    CATEGORY_CHOICES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('twin', 'Twin'),
        ('deluxe', 'Deluxe'),
        ('executive', 'Executive'),
        ('family_suite', 'Family Suite'),
        ('presidential', 'Presidential Suite'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Room Categories'

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)


class Amenity(TimeStampedModel):
    """Room and hotel amenities."""

    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='bi-check-circle')
    description = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Amenities'

    def __str__(self) -> str:
        return self.name


class Room(PublishableModel, SEOModel, TimeStampedModel):
    """Individual hotel rooms."""

    BED_TYPES = [
        ('single', 'Single Bed'),
        ('double', 'Double Bed'),
        ('queen', 'Queen Bed'),
        ('king', 'King Bed'),
        ('twin', 'Twin Beds'),
        ('sofa', 'Sofa Bed'),
    ]

    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
        ('blocked', 'Blocked'),
    ]

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    room_number = models.CharField(max_length=10, unique=True)
    category = models.ForeignKey(RoomCategory, on_delete=models.PROTECT, related_name='rooms')
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    size_sqm = models.PositiveIntegerField(help_text='Room size in square meters')
    bed_type = models.CharField(max_length=20, choices=BED_TYPES)
    max_occupancy = models.PositiveSmallIntegerField(default=2)
    max_adults = models.PositiveSmallIntegerField(default=2)
    max_children = models.PositiveSmallIntegerField(default=1)
    amenities = models.ManyToManyField(Amenity, blank=True, related_name='rooms')
    policies = models.TextField(blank=True, help_text='Cancellation and room policies')
    availability_status = models.CharField(
        max_length=20, choices=AVAILABILITY_CHOICES, default='available'
    )
    main_image = models.ImageField(upload_to='rooms/', blank=True)
    floor = models.PositiveSmallIntegerField(default=1)
    has_balcony = models.BooleanField(default=False)
    has_lake_view = models.BooleanField(default=False)

    class Meta:
        ordering = ['category__order', 'room_number']

    def __str__(self) -> str:
        return f'{self.name} (#{self.room_number})'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse('rooms:detail', kwargs={'slug': self.slug})


class RoomImage(TimeStampedModel):
    """Gallery images for a room."""

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='rooms/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self) -> str:
        return f'Image for {self.room.name}'
