"""
Abstract base models and shared utilities for the hotel website.
"""
from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    """Abstract model with created/updated timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PublishableModel(models.Model):
    """Abstract model for publishable content."""

    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['order']


class SEOModel(models.Model):
    """Abstract model for SEO fields."""

    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True

    def get_meta_title(self) -> str:
        return self.meta_title or str(self)

    def get_meta_description(self) -> str:
        return self.meta_description


def unique_slugify(instance, value: str, slug_field: str = 'slug') -> str:
    """Generate a unique slug for a model instance."""
    slug = slugify(value)
    model = instance.__class__
    unique_slug = slug
    counter = 1
    while model.objects.filter(**{slug_field: unique_slug}).exclude(pk=instance.pk).exists():
        unique_slug = f'{slug}-{counter}'
        counter += 1
    return unique_slug
