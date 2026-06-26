"""Assign local images from the images/ folder to database models."""
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from blog.models import BlogPost
from conference.models import ConferenceHall, EventPackage
from core.models import HeroSlider, HomeFeature, SpecialOffer, TourPackage
from gallery.models import GalleryCategory, GalleryImage
from restaurant.models import Restaurant
from rooms.models import Room


class Command(BaseCommand):
    help = 'Assign images from the images/ folder to hotel models based on filename'

    IMAGE_MAP = {
        'hero': 'hero.jpg',
        'main': 'main image.jpg',
        'rooms': 'rooms.jpg',
        'vip': 'vip room.jpg',
        'nature': 'nature.jpg',
        'additional': 'additional image.jpg',
    }

    def handle(self, *args, **options):
        self.images_dir = Path(settings.BASE_DIR) / 'images'
        if not self.images_dir.exists():
            self.stderr.write(self.style.ERROR(f'Images folder not found: {self.images_dir}'))
            return

        missing = [f for f in self.IMAGE_MAP.values() if not (self.images_dir / f).exists()]
        if missing:
            self.stderr.write(self.style.ERROR(f'Missing files: {", ".join(missing)}'))
            return

        self.stdout.write('Assigning local images to models...')
        self._assign_hero_slides()
        self._assign_restaurant()
        self._assign_rooms()
        self._assign_conference()
        self._assign_events()
        self._assign_tours()
        self._assign_gallery()
        self._assign_blog()
        self._assign_offers()
        self._assign_home_features()
        self.stdout.write(self.style.SUCCESS('Images assigned successfully!'))

    def _save_image(self, instance, field_name: str, image_key: str) -> None:
        filename = self.IMAGE_MAP[image_key]
        filepath = self.images_dir / filename
        with open(filepath, 'rb') as f:
            getattr(instance, field_name).save(filename, File(f), save=True)
        self.stdout.write(f'  {instance.__class__.__name__}: {instance} <- {filename}')

    def _assign_hero_slides(self):
        slides = list(HeroSlider.objects.filter(is_published=True).order_by('order'))
        keys = ['hero', 'main', 'nature']
        for slide, key in zip(slides, keys):
            self._save_image(slide, 'image', key)

    def _assign_restaurant(self):
        restaurant = Restaurant.load()
        self._save_image(restaurant, 'main_image', 'main')

    def _assign_rooms(self):
        vip_categories = ('executive', 'family_suite', 'presidential')
        for room in Room.objects.filter(is_published=True):
            key = 'vip' if room.category.category_type in vip_categories else 'rooms'
            self._save_image(room, 'main_image', key)

    def _assign_conference(self):
        keys = ['main', 'additional', 'main', 'additional', 'main']
        for hall, key in zip(ConferenceHall.objects.filter(is_published=True).order_by('order'), keys):
            self._save_image(hall, 'main_image', key)

    def _assign_events(self):
        keys = ['additional', 'main', 'additional', 'main', 'additional']
        for package, key in zip(EventPackage.objects.filter(is_published=True).order_by('order'), keys):
            self._save_image(package, 'image', key)

    def _assign_tours(self):
        for tour in TourPackage.objects.filter(is_published=True):
            self._save_image(tour, 'image', 'nature')

    def _assign_gallery(self):
        category_images = {
            'hotel': ['main', 'additional'],
            'rooms': ['rooms', 'vip'],
            'restaurant': ['additional', 'main'],
            'events': ['additional', 'main'],
            'nature': ['nature', 'nature'],
            'conference': ['main', 'additional'],
            'pool': ['nature', 'additional'],
            'garden': ['nature', 'main'],
        }
        for category in GalleryCategory.objects.filter(is_published=True):
            keys = category_images.get(category.category_type, ['additional', 'main'])
            images = list(category.images.filter(is_published=True).order_by('order'))
            for img, key in zip(images, keys * ((len(images) // len(keys)) + 1)):
                self._save_image(img, 'image', key)

    def _assign_blog(self):
        keys = ['nature', 'main', 'additional', 'rooms', 'nature']
        posts = list(BlogPost.objects.filter(is_published=True).order_by('-published_at'))
        for post, key in zip(posts, keys * ((len(posts) // len(keys)) + 1)):
            self._save_image(post, 'featured_image', key)

    def _assign_offers(self):
        keys = ['additional', 'main', 'nature', 'rooms', 'vip']
        for offer, key in zip(SpecialOffer.objects.filter(is_published=True).order_by('order'), keys):
            self._save_image(offer, 'image', key)

    def _assign_home_features(self):
        feature_images = {
            'Luxury Rooms': 'rooms',
            'Fine Dining': 'additional',
            'Conference Hall': 'main',
            'Swimming Pool': 'nature',
            'Garden': 'nature',
            'Airport Shuttle': 'main',
            'Lake Chamo Tours': 'nature',
            'Nech Sar Park': 'nature',
        }
        for feature in HomeFeature.objects.filter(is_published=True):
            key = feature_images.get(feature.title, 'main')
            self._save_image(feature, 'image', key)
