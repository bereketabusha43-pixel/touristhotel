"""
Blog models for travel guides and hotel news.
"""
from django.db import models
from django.urls import reverse
from django.utils import timezone

from ckeditor.fields import RichTextField

from core.mixins import PublishableModel, SEOModel, TimeStampedModel, unique_slugify


class BlogCategory(PublishableModel, TimeStampedModel):
    """Blog post categories."""

    CATEGORY_CHOICES = [
        ('travel', 'Travel Guides'),
        ('news', 'Hotel News'),
        ('tourism', 'Tourism'),
        ('attractions', 'Local Attractions'),
        ('restaurant', 'Restaurant'),
        ('events', 'Events'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Blog Categories'

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)


class BlogPost(PublishableModel, SEOModel, TimeStampedModel):
    """Blog articles with rich text content."""

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=270, unique=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.PROTECT, related_name='posts')
    author = models.CharField(max_length=100, default='Arba Minch Tourist Hotel')
    excerpt = models.TextField(max_length=500, blank=True)
    content = RichTextField()
    featured_image = models.ImageField(upload_to='blog/', blank=True)
    published_at = models.DateTimeField(default=timezone.now)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-published_at']

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse('blog:detail', kwargs={'slug': self.slug})
