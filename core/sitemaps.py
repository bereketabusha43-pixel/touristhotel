"""SEO sitemaps."""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import BlogPost
from conference.models import ConferenceHall, EventPackage
from core.models import SpecialOffer, TourPackage
from rooms.models import Room


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'home:index', 'home:about', 'home:experiences',
            'rooms:list', 'restaurant:index', 'conference:index',
            'conference:events', 'gallery:list', 'blog:list', 'contact:index',
            'booking:search',
        ]

    def location(self, item):
        return reverse(item)


class RoomSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Room.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class ConferenceSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return ConferenceHall.objects.filter(is_published=True)


class EventSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return EventPackage.objects.filter(is_published=True)


class TourSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return TourPackage.objects.filter(is_published=True)


class OfferSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return SpecialOffer.objects.filter(is_published=True)
