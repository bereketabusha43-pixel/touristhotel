"""
Restaurant models: menu items and table reservations.
"""
from django.db import models

from core.mixins import PublishableModel, TimeStampedModel


class Restaurant(TimeStampedModel):
    """Restaurant information (singleton)."""

    name = models.CharField(max_length=200, default='Arba Minch Tourist Hotel Restaurant')
    description = models.TextField(blank=True)
    breakfast_hours = models.CharField(max_length=100, default='6:30 AM – 10:00 AM')
    lunch_hours = models.CharField(max_length=100, default='12:00 PM – 3:00 PM')
    dinner_hours = models.CharField(max_length=100, default='6:30 PM – 10:30 PM')
    main_image = models.ImageField(upload_to='restaurant/', blank=True)
    chef_name = models.CharField(max_length=100, blank=True)
    chef_special = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurant'

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls) -> 'Restaurant':
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class MenuCategory(PublishableModel, TimeStampedModel):
    """Menu categories (Breakfast, Lunch, Ethiopian, etc.)."""

    CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('ethiopian', 'Traditional Ethiopian'),
        ('international', 'International'),
        ('coffee', 'Coffee & Beverages'),
        ('desserts', 'Desserts'),
        ('chef_special', 'Chef Specials'),
    ]

    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Menu Categories'

    def __str__(self) -> str:
        return self.name


class MenuItem(PublishableModel, TimeStampedModel):
    """Individual menu items."""

    name = models.CharField(max_length=200)
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menu/', blank=True)
    is_vegetarian = models.BooleanField(default=False)
    is_spicy = models.BooleanField(default=False)
    is_chef_special = models.BooleanField(default=False)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self) -> str:
        return self.name


class RestaurantReservation(TimeStampedModel):
    """Table reservation at the restaurant."""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveSmallIntegerField(default=2)
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self) -> str:
        return f'{self.name} — {self.date} at {self.time}'
