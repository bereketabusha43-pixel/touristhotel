"""
Gallery models for categorized hotel imagery.
"""
from django.db import models

from core.mixins import PublishableModel, TimeStampedModel


class GalleryCategory(PublishableModel, TimeStampedModel):
    """Gallery image categories."""

    CATEGORY_CHOICES = [
        ('hotel', 'Hotel'),
        ('rooms', 'Rooms'),
        ('restaurant', 'Restaurant'),
        ('events', 'Events'),
        ('nature', 'Nature'),
        ('conference', 'Conference'),
        ('pool', 'Swimming Pool'),
        ('garden', 'Garden'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Gallery Categories'

    def __str__(self) -> str:
        return self.name


class GalleryImage(PublishableModel, TimeStampedModel):
    """Individual gallery images."""

    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    caption = models.TextField(blank=True)
    alt_text = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self) -> str:
        return self.title
