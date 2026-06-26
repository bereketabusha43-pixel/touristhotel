"""Tests for the hotel website."""
from datetime import date, timedelta
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from booking.models import Booking, Guest
from booking.services import BookingService
from core.models import SiteSettings
from rooms.models import Room, RoomCategory


class SiteSettingsTest(TestCase):
    def test_singleton_load(self):
        settings = SiteSettings.load()
        self.assertEqual(settings.pk, 1)


class RoomModelTest(TestCase):
    def setUp(self):
        self.category = RoomCategory.objects.create(
            name='Deluxe', slug='deluxe', category_type='deluxe',
        )
        self.room = Room.objects.create(
            name='Deluxe 101', slug='deluxe-101', room_number='101',
            category=self.category, description='A nice room',
            price_per_night=Decimal('5000'), size_sqm=45,
            bed_type='queen', max_occupancy=2,
        )

    def test_room_str(self):
        self.assertIn('Deluxe 101', str(self.room))

    def test_room_url(self):
        self.assertEqual(self.room.get_absolute_url(), '/rooms/deluxe-101/')


class BookingServiceTest(TestCase):
    def setUp(self):
        self.category = RoomCategory.objects.create(
            name='Single', slug='single', category_type='single',
        )
        self.room = Room.objects.create(
            name='Single 201', slug='single-201', room_number='201',
            category=self.category, description='Single room',
            price_per_night=Decimal('2500'), size_sqm=25,
            bed_type='single', max_occupancy=1, is_published=True,
        )
        self.check_in = date.today() + timedelta(days=7)
        self.check_out = self.check_in + timedelta(days=3)

    def test_room_available_when_no_bookings(self):
        self.assertTrue(BookingService.is_room_available(self.room, self.check_in, self.check_out))

    def test_room_unavailable_when_booked(self):
        guest = Guest.objects.create(
            first_name='Test', last_name='User', email='test@test.com', phone='123',
        )
        Booking.objects.create(
            guest=guest, room=self.room, check_in=self.check_in,
            check_out=self.check_out, adults=1, total_price=Decimal('7500'),
            status='confirmed',
        )
        self.assertFalse(BookingService.is_room_available(self.room, self.check_in, self.check_out))

    def test_calculate_total(self):
        total = BookingService.calculate_total(self.room, self.check_in, self.check_out)
        self.assertEqual(total, Decimal('7500'))

    def test_get_available_rooms(self):
        rooms = BookingService.get_available_rooms(self.check_in, self.check_out)
        self.assertIn(self.room, rooms)


class ViewTest(TestCase):
    def test_homepage(self):
        response = self.client.get(reverse('home:index'))
        self.assertEqual(response.status_code, 200)

    def test_rooms_list(self):
        response = self.client.get(reverse('rooms:list'))
        self.assertEqual(response.status_code, 200)

    def test_booking_search(self):
        response = self.client.get(reverse('booking:search'))
        self.assertEqual(response.status_code, 200)

    def test_contact_page(self):
        response = self.client.get(reverse('contact:index'))
        self.assertEqual(response.status_code, 200)

    def test_robots_txt(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sitemap')
