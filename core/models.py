"""
Core models: site settings, testimonials, offers, tours, FAQs, and homepage content.
"""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from core.mixins import PublishableModel, SEOModel, TimeStampedModel, unique_slugify


class SiteSettings(models.Model):
    """Singleton model for hotel-wide settings."""

    hotel_name = models.CharField(max_length=200, default='Arba Minch Tourist Hotel')
    tagline = models.CharField(max_length=255, default='Where Comfort Meets Nature')
    description = models.TextField(blank=True)
    address = models.TextField(default='Arba Minch, Southern Nations, Ethiopia')
    phone = models.CharField(max_length=30, default='+251 46 881 0000')
    phone_secondary = models.CharField(max_length=30, blank=True)
    email = models.EmailField(default='info@arbaminchhotel.com')
    whatsapp = models.CharField(max_length=30, blank=True)
    emergency_contact = models.CharField(max_length=30, blank=True)
    logo = models.ImageField(upload_to='site/', blank=True)
    favicon = models.ImageField(upload_to='site/', blank=True)
    google_maps_embed = models.TextField(blank=True, help_text='Google Maps embed iframe code')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    business_hours = models.TextField(blank=True)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    star_rating = models.PositiveSmallIntegerField(default=4)
    about_history = models.TextField(blank=True)
    about_mission = models.TextField(blank=True)
    about_vision = models.TextField(blank=True)
    about_csr = models.TextField(blank=True, verbose_name='Corporate Social Responsibility')
    why_choose_us = models.TextField(blank=True)
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self) -> str:
        return self.hotel_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls) -> 'SiteSettings':
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SocialMedia(TimeStampedModel):
    """Social media links."""

    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter/X'),
        ('youtube', 'YouTube'),
        ('linkedin', 'LinkedIn'),
        ('tiktok', 'TikTok'),
        ('tripadvisor', 'TripAdvisor'),
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    icon_class = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Social Media'

    def __str__(self) -> str:
        return self.get_platform_display()


class HeroSlider(PublishableModel, TimeStampedModel):
    """Homepage hero slider items."""

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='hero/')
    video_url = models.URLField(blank=True, help_text='Optional video URL for hero background')
    cta_text = models.CharField(max_length=50, blank=True, default='Book Now')
    cta_link = models.CharField(max_length=200, blank=True, default='/booking/')

    class Meta:
        ordering = ['order']

    def __str__(self) -> str:
        return self.title


class HomeFeature(PublishableModel, TimeStampedModel):
    """Featured sections on the homepage."""

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='bi-star')
    image = models.ImageField(upload_to='features/', blank=True)
    link = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self) -> str:
        return self.title


class Award(TimeStampedModel):
    """Hotel awards and recognitions."""

    title = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    organization = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='awards/', blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-year', 'order']

    def __str__(self) -> str:
        return f'{self.title} ({self.year})'


class TeamMember(PublishableModel, TimeStampedModel):
    """Management and team members for About page."""

    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='team/', blank=True)
    email = models.EmailField(blank=True)
    is_management = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self) -> str:
        return self.name


class Testimonial(PublishableModel, TimeStampedModel):
    """Guest testimonials."""

    guest_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='testimonials/', blank=True)
    rating = models.PositiveSmallIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    content = models.TextField()
    stay_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self) -> str:
        return f'{self.guest_name} — {self.rating}★'


class SpecialOffer(PublishableModel, SEOModel, TimeStampedModel):
    """Special offers and promotions."""

    OFFER_TYPES = [
        ('weekend', 'Weekend Package'),
        ('family', 'Family Package'),
        ('conference', 'Conference Package'),
        ('holiday', 'Holiday Discount'),
        ('seasonal', 'Seasonal Promotion'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPES, default='seasonal')
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='offers/', blank=True)
    discount_percent = models.PositiveSmallIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valid_from = models.DateField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)
    terms = models.TextField(blank=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse('home:offer_detail', kwargs={'slug': self.slug})


class TourPackage(PublishableModel, SEOModel, TimeStampedModel):
    """Experience and tour packages."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='tours/', blank=True)
    duration = models.CharField(max_length=50, blank=True, help_text='e.g. Half Day, Full Day')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_guests = models.PositiveIntegerField(default=10)
    includes = models.TextField(blank=True, help_text='One item per line')
    location = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse('home:experience_detail', kwargs={'slug': self.slug})

    def get_includes_list(self) -> list[str]:
        return [line.strip() for line in self.includes.splitlines() if line.strip()]


class FAQ(PublishableModel, TimeStampedModel):
    """Frequently asked questions."""

    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('booking', 'Booking'),
        ('rooms', 'Rooms'),
        ('dining', 'Dining'),
        ('conference', 'Conference'),
        ('tours', 'Tours'),
    ]

    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')

    class Meta:
        ordering = ['order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self) -> str:
        return self.question
