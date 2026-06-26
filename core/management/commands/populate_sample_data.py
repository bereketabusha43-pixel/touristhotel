"""Management command to populate sample hotel data."""
from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from blog.models import BlogCategory, BlogPost
from conference.models import ConferenceHall, EventPackage
from core.models import (
    Award,
    FAQ,
    HeroSlider,
    HomeFeature,
    SiteSettings,
    SocialMedia,
    SpecialOffer,
    TeamMember,
    Testimonial,
    TourPackage,
)
from gallery.models import GalleryCategory, GalleryImage
from restaurant.models import MenuCategory, MenuItem, Restaurant
from rooms.models import Amenity, Room, RoomCategory


class Command(BaseCommand):
    help = 'Populate the database with realistic sample hotel data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        self._create_site_settings()
        self._create_social_media()
        self._create_hero_slides()
        self._create_features()
        self._create_amenities()
        categories = self._create_room_categories()
        self._create_rooms(categories)
        self._create_restaurant()
        self._create_conference_halls()
        self._create_event_packages()
        self._create_tour_packages()
        self._create_gallery()
        self._create_blog()
        self._create_testimonials()
        self._create_offers()
        self._create_faqs()
        self._create_awards()
        self._create_team()

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write('Run "python manage.py assign_local_images" to attach images from the images/ folder.')

    def _create_site_settings(self):
        SiteSettings.objects.update_or_create(pk=1, defaults={
            'hotel_name': 'Arba Minch Tourist Hotel',
            'tagline': 'Where Comfort Meets Nature',
            'description': (
                'Arba Minch Tourist Hotel is one of the largest and most prestigious hotels '
                'in Southern Ethiopia, offering world-class hospitality amidst breathtaking natural beauty.'
            ),
            'address': 'Secha Street, Arba Minch, Southern Nations, Nationalities and Peoples Region, Ethiopia',
            'phone': '+251 46 881 0000',
            'phone_secondary': '+251 46 881 0001',
            'email': 'info@arbaminchhotel.com',
            'whatsapp': '251911234567',
            'emergency_contact': '+251 46 881 0099',
            'star_rating': 4,
            'business_hours': 'Front Desk: 24/7\nRestaurant: 6:30 AM – 10:30 PM\nConcierge: 7:00 AM – 9:00 PM',
            'about_history': (
                'Founded in 1985, Arba Minch Tourist Hotel has been the premier destination for travelers '
                'exploring Southern Ethiopia. Over the decades, we have welcomed dignitaries, tourists, '
                'and business travelers from around the world, building a reputation for exceptional Ethiopian hospitality.'
            ),
            'about_mission': (
                'To provide unparalleled hospitality experiences that showcase the natural beauty '
                'and rich culture of Arba Minch while exceeding guest expectations.'
            ),
            'about_vision': (
                'To be the leading luxury hotel in East Africa, recognized for sustainable tourism '
                'and authentic Ethiopian experiences.'
            ),
            'about_csr': (
                'We actively support local communities through employment, sourcing local produce, '
                'and environmental conservation initiatives around Lake Chamo and Nech Sar National Park.'
            ),
            'why_choose_us': (
                '• Prime location overlooking Lake Abaya and Lake Chamo\n'
                '• 50 elegantly appointed rooms and suites\n'
                '• Award-winning restaurant with Ethiopian and international cuisine\n'
                '• State-of-the-art conference facilities\n'
                '• Complimentary airport shuttle service\n'
                '• Expert concierge for tours and excursions'
            ),
            'meta_title': 'Arba Minch Tourist Hotel — Luxury Hotel in Ethiopia',
            'meta_description': 'Experience luxury hospitality at Arba Minch Tourist Hotel. Premium rooms, dining, conference facilities, and tours in Southern Ethiopia.',
        })

    def _create_social_media(self):
        platforms = [
            ('facebook', 'https://facebook.com/arbaminchhotel'),
            ('instagram', 'https://instagram.com/arbaminchhotel'),
            ('twitter', 'https://twitter.com/arbaminchhotel'),
            ('youtube', 'https://youtube.com/arbaminchhotel'),
            ('tripadvisor', 'https://tripadvisor.com/arbaminchhotel'),
        ]
        for i, (platform, url) in enumerate(platforms):
            SocialMedia.objects.get_or_create(platform=platform, defaults={'url': url, 'order': i})

    def _create_hero_slides(self):
        slides = [
            ('Experience Luxury in the Heart of Arba Minch', 'Where Comfort Meets Nature'),
            ('Stunning Views of the Rift Valley', 'Wake Up to Paradise Every Morning'),
            ('World-Class Dining Experience', 'Taste the Flavors of Ethiopia'),
        ]
        for i, (title, subtitle) in enumerate(slides):
            HeroSlider.objects.get_or_create(title=title, defaults={
                'subtitle': subtitle, 'order': i, 'is_published': True, 'is_featured': True,
            })

    def _create_features(self):
        features = [
            ('Luxury Rooms', 'bi-door-open', 'Elegantly designed rooms with modern amenities'),
            ('Fine Dining', 'bi-cup-hot', 'Ethiopian and international cuisine'),
            ('Conference Hall', 'bi-people', 'State-of-the-art meeting facilities'),
            ('Swimming Pool', 'bi-water', 'Refreshing pool with valley views'),
            ('Garden', 'bi-flower1', 'Lush tropical gardens'),
            ('Airport Shuttle', 'bi-airplane', 'Complimentary airport transfers'),
            ('Lake Chamo Tours', 'bi-binoculars', 'Guided boat tours and wildlife watching'),
            ('Nech Sar Park', 'bi-tree', 'Gateway to Nech Sar National Park'),
        ]
        for i, (title, icon, desc) in enumerate(features):
            HomeFeature.objects.get_or_create(title=title, defaults={
                'icon': icon, 'description': desc, 'order': i, 'is_published': True,
            })

    def _create_amenities(self):
        items = [
            ('Free WiFi', 'bi-wifi'), ('Air Conditioning', 'bi-snow'), ('Mini Bar', 'bi-cup-straw'),
            ('Room Service', 'bi-bell'), ('Flat Screen TV', 'bi-tv'), ('Safe', 'bi-shield-lock'),
            ('Coffee Maker', 'bi-cup-hot'), ('Hair Dryer', 'bi-wind'), ('Bathtub', 'bi-droplet'),
            ('Balcony', 'bi-door-open'), ('Lake View', 'bi-water'), ('Work Desk', 'bi-laptop'),
        ]
        for i, (name, icon) in enumerate(items):
            Amenity.objects.get_or_create(name=name, defaults={'icon': icon, 'order': i})

    def _create_room_categories(self):
        cats = {}
        data = [
            ('Single Room', 'single'), ('Double Room', 'double'), ('Twin Room', 'twin'),
            ('Deluxe Room', 'deluxe'), ('Executive Suite', 'executive'),
            ('Family Suite', 'family_suite'), ('Presidential Suite', 'presidential'),
        ]
        for i, (name, ctype) in enumerate(data):
            cat, _ = RoomCategory.objects.get_or_create(
                category_type=ctype,
                defaults={'name': name, 'slug': slugify(name), 'order': i,
                          'description': f'Spacious and comfortable {name.lower()} with modern amenities.'},
            )
            cats[ctype] = cat
        return cats

    def _create_rooms(self, categories):
        if Room.objects.count() >= 50:
            return
        bed_map = {
            'single': 'single', 'double': 'double', 'twin': 'twin',
            'deluxe': 'queen', 'executive': 'king', 'family_suite': 'king', 'presidential': 'king',
        }
        price_map = {
            'single': 2500, 'double': 3500, 'twin': 3500, 'deluxe': 5000,
            'executive': 7500, 'family_suite': 9000, 'presidential': 15000,
        }
        size_map = {
            'single': 25, 'double': 35, 'twin': 35, 'deluxe': 45,
            'executive': 55, 'family_suite': 70, 'presidential': 100,
        }
        occ_map = {
            'single': 1, 'double': 2, 'twin': 2, 'deluxe': 2,
            'executive': 2, 'family_suite': 4, 'presidential': 4,
        }
        cat_types = list(categories.keys())
        amenities = list(Amenity.objects.all())
        for i in range(1, 51):
            floor = (i - 1) // 10 + 1
            ctype = cat_types[(i - 1) % len(cat_types)]
            cat = categories[ctype]
            num = f'{floor}{i % 10:02d}' if i % 10 else f'{floor}10'
            room, created = Room.objects.get_or_create(
                room_number=num,
                defaults={
                    'name': f'{cat.name} {num}',
                    'slug': slugify(f'{cat.name}-{num}'),
                    'category': cat,
                    'description': (
                        f'Experience comfort in our {cat.name.lower()}, featuring elegant furnishings, '
                        f'modern amenities, and stunning views of the Arba Minch landscape.'
                    ),
                    'short_description': f'Comfortable {cat.name.lower()} with premium amenities.',
                    'price_per_night': Decimal(str(price_map[ctype] + (i % 5) * 200)),
                    'size_sqm': size_map[ctype],
                    'bed_type': bed_map[ctype],
                    'max_occupancy': occ_map[ctype],
                    'max_adults': occ_map[ctype],
                    'max_children': 2 if occ_map[ctype] >= 2 else 0,
                    'floor': floor,
                    'has_balcony': ctype in ('deluxe', 'executive', 'family_suite', 'presidential'),
                    'has_lake_view': i % 3 == 0,
                    'is_published': True,
                    'is_featured': i <= 8,
                    'policies': 'Check-in: 2:00 PM | Check-out: 12:00 PM | Free cancellation up to 24 hours before arrival.',
                },
            )
            if created and amenities:
                room.amenities.set(amenities[:6 + (i % 6)])

    def _create_restaurant(self):
        Restaurant.objects.update_or_create(pk=1, defaults={
            'name': 'Abaya Restaurant',
            'description': (
                'Our signature restaurant offers an exquisite dining experience featuring traditional '
                'Ethiopian cuisine alongside international favorites. Enjoy panoramic views of the '
                'Rift Valley while savoring dishes prepared with locally sourced ingredients.'
            ),
            'chef_name': 'Chef Dawit Bekele',
            'chef_special': 'Try our famous Doro Wat with fresh injera, or the Lake Chamo grilled tilapia.',
        })
        menu_cats = {
            'breakfast': 'Breakfast',
            'lunch': 'Lunch',
            'dinner': 'Dinner',
            'ethiopian': 'Traditional Ethiopian',
            'international': 'International Cuisine',
            'coffee': 'Coffee & Beverages',
            'desserts': 'Desserts',
        }
        menu_items = {
            'breakfast': [
                ('Full Ethiopian Breakfast', 350, 'Injera, eggs, firfir, fresh juice'),
                ('Continental Breakfast', 400, 'Pastries, fruits, yogurt, coffee'),
                ('Pancake Stack', 300, 'Fluffy pancakes with honey and fruits'),
            ],
            'ethiopian': [
                ('Doro Wat', 450, 'Spicy chicken stew with boiled egg'),
                ('Tibs', 500, 'Sautéed meat with vegetables and spices'),
                ('Kitfo', 550, 'Minced beef with spiced butter'),
                ('Shiro', 300, 'Chickpea stew with injera'),
                ('Beyaynetu', 400, 'Mixed vegetarian platter'),
            ],
            'international': [
                ('Grilled Lake Tilapia', 600, 'Fresh catch from Lake Chamo'),
                ('Beef Tenderloin', 750, 'Grilled with rosemary and vegetables'),
                ('Pasta Alfredo', 450, 'Creamy fettuccine with parmesan'),
                ('Caesar Salad', 350, 'Crisp romaine with classic dressing'),
            ],
            'coffee': [
                ('Ethiopian Coffee Ceremony', 200, 'Traditional buna ceremony'),
                ('Macchiato', 80, 'Ethiopian style macchiato'),
                ('Fresh Mango Juice', 150, 'Seasonal tropical fruits'),
            ],
            'desserts': [
                ('Honey Wine Cake', 250, 'Local tej-infused dessert'),
                ('Fresh Fruit Platter', 200, 'Seasonal tropical fruits'),
            ],
        }
        for ctype, name in menu_cats.items():
            cat, _ = MenuCategory.objects.get_or_create(
                category_type=ctype, defaults={'name': name, 'is_published': True},
            )
            if ctype in menu_items:
                for j, (iname, price, desc) in enumerate(menu_items[ctype]):
                    MenuItem.objects.get_or_create(
                        name=iname, category=cat,
                        defaults={'price': Decimal(str(price)), 'description': desc,
                                    'is_published': True, 'order': j},
                    )

    def _create_conference_halls(self):
        halls = [
            ('Abaya Conference Hall', 300, 450, 25000),
            ('Chamo Meeting Room', 50, 80, 8000),
            ('Nech Sar Boardroom', 20, 40, 5000),
            ('Rift Valley Ballroom', 500, 700, 45000),
            ('Executive Meeting Suite', 15, 30, 4000),
        ]
        for i, (name, cap, sqm, price) in enumerate(halls):
            ConferenceHall.objects.get_or_create(
                slug=slugify(name),
                defaults={
                    'name': name, 'capacity': cap, 'size_sqm': sqm,
                    'price_per_day': Decimal(str(price)),
                    'price_per_half_day': Decimal(str(price // 2)),
                    'description': f'{name} offers a professional setting for conferences, meetings, and events.',
                    'equipment': 'Projector\nSound System\nWiFi\nAir Conditioning\nWhiteboard\nPodium',
                    'is_published': True, 'is_featured': i < 2, 'order': i,
                },
            )

    def _create_event_packages(self):
        events = [
            ('Royal Wedding Package', 'wedding', 150000, 300),
            ('Graduation Celebration', 'graduation', 50000, 150),
            ('Birthday Bash', 'birthday', 30000, 80),
            ('Corporate Gala', 'corporate', 80000, 200),
            ('Garden Outdoor Event', 'outdoor', 60000, 250),
        ]
        for i, (title, etype, price, guests) in enumerate(events):
            EventPackage.objects.get_or_create(
                slug=slugify(title),
                defaults={
                    'title': title, 'event_type': etype,
                    'price': Decimal(str(price)), 'max_guests': guests,
                    'description': f'Our {title.lower()} provides everything you need for a memorable event.',
                    'short_description': f'Complete {etype} package for up to {guests} guests.',
                    'includes': 'Venue Setup\nCatering\nDecoration\nSound System\nEvent Coordinator',
                    'is_published': True, 'order': i,
                },
            )

    def _create_tour_packages(self):
        tours = [
            ('Lake Chamo Boat Tour', 'Half Day', 1500, 'Lake Chamo'),
            ('Nech Sar National Park Safari', 'Full Day', 2500, 'Nech Sar National Park'),
            ('Dorze Village Cultural Tour', 'Full Day', 2000, 'Dorze Village'),
            ('Forty Springs Hiking', 'Half Day', 1200, 'Forty Springs'),
            ('Bird Watching Expedition', 'Full Day', 1800, 'Arba Minch'),
        ]
        for i, (title, duration, price, location) in enumerate(tours):
            TourPackage.objects.get_or_create(
                slug=slugify(title),
                defaults={
                    'title': title, 'duration': duration,
                    'price': Decimal(str(price)), 'location': location,
                    'description': f'Explore {location} with our expert guides on this {duration.lower()} tour.',
                    'short_description': f'{duration} guided tour of {location}.',
                    'includes': 'Transportation\nGuide\nEntrance Fees\nRefreshments',
                    'is_published': True, 'is_featured': True, 'order': i,
                },
            )

    def _create_gallery(self):
        cats = {
            'hotel': 'Hotel', 'rooms': 'Rooms', 'restaurant': 'Restaurant',
            'events': 'Events', 'nature': 'Nature', 'conference': 'Conference',
            'pool': 'Swimming Pool', 'garden': 'Garden',
        }
        cat_objs = {}
        for ctype, name in cats.items():
            cat, _ = GalleryCategory.objects.get_or_create(
                slug=ctype, defaults={'name': name, 'category_type': ctype, 'is_published': True},
            )
            cat_objs[ctype] = cat

        if GalleryImage.objects.count() >= 40:
            return
        cat_list = list(cat_objs.values())
        for i in range(40):
            cat = cat_list[i % len(cat_list)]
            GalleryImage.objects.get_or_create(
                title=f'{cat.name} Photo {i + 1}',
                category=cat,
                defaults={
                    'caption': f'Beautiful view of our {cat.name.lower()}',
                    'alt_text': f'Arba Minch Tourist Hotel {cat.name.lower()}',
                    'is_published': True, 'is_featured': i < 8, 'order': i,
                },
            )

    def _create_blog(self):
        cats = {
            'travel': 'Travel Guides', 'news': 'Hotel News', 'tourism': 'Tourism',
            'attractions': 'Local Attractions', 'restaurant': 'Restaurant', 'events': 'Events',
        }
        cat_objs = {}
        for ctype, name in cats.items():
            cat, _ = BlogCategory.objects.get_or_create(
                category_type=ctype, defaults={'name': name, 'slug': slugify(name), 'is_published': True},
            )
            cat_objs[ctype] = cat

        posts = [
            ('Top 10 Things to Do in Arba Minch', 'travel'),
            ('Exploring Lake Chamo: A Complete Guide', 'attractions'),
            ('Nech Sar National Park Wildlife Guide', 'attractions'),
            ('The Magic of Ethiopian Coffee Culture', 'restaurant'),
            ('Dorze Village: Weaving Traditions', 'tourism'),
            ('Best Time to Visit Southern Ethiopia', 'travel'),
            ('Our New Presidential Suite Unveiled', 'news'),
            ('Sustainable Tourism in Arba Minch', 'tourism'),
            ('Traditional Ethiopian Food You Must Try', 'restaurant'),
            ('Planning Your Rift Valley Adventure', 'travel'),
            ('Bird Watching in Arba Minch', 'attractions'),
            ('Hotel Renovation Update 2025', 'news'),
            ('Corporate Events at AMTH', 'events'),
            ('Forty Springs: Nature\'s Hidden Gem', 'attractions'),
            ('Ethiopian New Year Celebration at AMTH', 'events'),
        ]
        for i, (title, ctype) in enumerate(posts):
            BlogPost.objects.get_or_create(
                slug=slugify(title),
                defaults={
                    'title': title, 'category': cat_objs[ctype],
                    'excerpt': f'Discover everything about {title.lower()} in this comprehensive guide.',
                    'content': f'<p>Welcome to our guide on {title.lower()}. Arba Minch offers incredible experiences for every traveler.</p><p>Whether you are visiting for business or leisure, this article will help you make the most of your stay at Arba Minch Tourist Hotel.</p>',
                    'is_published': True, 'is_featured': i < 3,
                    'published_at': timezone.now() - timedelta(days=i * 3),
                },
            )

    def _create_testimonials(self):
        guests = [
            ('Sarah Johnson', 'United Kingdom', 5),
            ('Hans Mueller', 'Germany', 5),
            ('Yuki Tanaka', 'Japan', 4),
            ('Maria Santos', 'Brazil', 5),
            ('Ahmed Hassan', 'Egypt', 5),
            ('Emily Chen', 'China', 4),
            ('Pierre Dubois', 'France', 5),
            ('Anna Kowalski', 'Poland', 5),
            ('David O\'Brien', 'Ireland', 4),
            ('Fatima Al-Rashid', 'UAE', 5),
        ]
        reviews = [
            'Absolutely stunning hotel with breathtaking views of the Rift Valley. The staff went above and beyond.',
            'The Ethiopian coffee ceremony was a highlight of our stay. Rooms are spacious and immaculately clean.',
            'Perfect base for exploring Nech Sar National Park. The restaurant serves amazing local cuisine.',
            'We hosted our corporate retreat here and everything was flawless. Excellent conference facilities.',
            'The lake view from our deluxe room was magical. Highly recommend the boat tour on Lake Chamo.',
        ]
        countries = ['USA', 'Canada', 'Australia', 'India', 'Kenya', 'South Africa', 'Sweden', 'Norway', 'Italy', 'Spain']
        for i in range(20):
            if i < len(guests):
                name, country, rating = guests[i]
            else:
                name, country, rating = f'Guest {i+1}', countries[i % len(countries)], 4 + (i % 2)
            Testimonial.objects.get_or_create(
                guest_name=name,
                defaults={
                    'country': country, 'rating': rating,
                    'content': reviews[i % len(reviews)],
                    'is_published': True, 'is_featured': i < 6, 'order': i,
                    'stay_date': date.today() - timedelta(days=30 * (i + 1)),
                },
            )

    def _create_offers(self):
        offers = [
            ('Weekend Escape Package', 'weekend', 15, 8000),
            ('Family Fun Package', 'family', 20, 12000),
            ('Conference Delegate Rate', 'conference', 25, None),
            ('Ethiopian New Year Special', 'holiday', 30, 6000),
            ('Summer Season Promotion', 'seasonal', 10, 5000),
        ]
        for i, (title, otype, discount, price) in enumerate(offers):
            SpecialOffer.objects.get_or_create(
                slug=slugify(title),
                defaults={
                    'title': title, 'offer_type': otype, 'discount_percent': discount,
                    'price': Decimal(str(price)) if price else None,
                    'description': f'Take advantage of our {title.lower()} with exclusive savings.',
                    'short_description': f'Save {discount}% on your stay.',
                    'valid_from': date.today(),
                    'valid_until': date.today() + timedelta(days=90),
                    'is_published': True, 'is_featured': i < 3, 'order': i,
                },
            )

    def _create_faqs(self):
        faqs = [
            ('What are the check-in and check-out times?', 'general',
             'Check-in is from 2:00 PM and check-out is by 12:00 PM. Early check-in and late check-out may be arranged upon request.'),
            ('Do you offer airport transfers?', 'general',
             'Yes, we provide complimentary airport shuttle service. Please inform us of your flight details when booking.'),
            ('Is WiFi available?', 'rooms', 'Free high-speed WiFi is available throughout the hotel.'),
            ('Can I cancel my booking?', 'booking',
             'Free cancellation is available up to 24 hours before check-in. Late cancellations may incur a one-night charge.'),
            ('Do you have conference facilities?', 'conference',
             'Yes, we have 5 conference halls ranging from intimate boardrooms to a 500-capacity ballroom.'),
            ('What dining options are available?', 'dining',
             'Our restaurant serves breakfast, lunch, and dinner with Ethiopian and international cuisine. Room service is available 24/7.'),
            ('Are pets allowed?', 'general', 'Unfortunately, we do not allow pets except service animals.'),
            ('What tours do you offer?', 'tours',
             'We offer guided tours to Lake Chamo, Nech Sar National Park, Dorze Village, and more.'),
        ]
        categories = ['general', 'booking', 'rooms', 'dining', 'conference', 'tours']
        for i in range(15):
            if i < len(faqs):
                q, cat, a = faqs[i]
            else:
                q, cat, a = f'FAQ Question {i+1}?', categories[i % len(categories)], f'Answer to question {i+1}.'
            FAQ.objects.get_or_create(question=q, defaults={'answer': a, 'category': cat, 'is_published': True, 'order': i})

    def _create_awards(self):
        awards = [
            ('Best Hotel in Southern Ethiopia', 2024, 'Ethiopian Tourism Board'),
            ('Excellence in Hospitality', 2023, 'African Hotel Awards'),
            ('Green Hotel Certification', 2023, 'Eco Tourism Ethiopia'),
            ('TripAdvisor Certificate of Excellence', 2024, 'TripAdvisor'),
        ]
        for i, (title, year, org) in enumerate(awards):
            Award.objects.get_or_create(title=title, year=year, defaults={'organization': org, 'order': i})

    def _create_team(self):
        team = [
            ('Abebe Tadesse', 'General Manager', True),
            ('Sara Mekonnen', 'Operations Director', True),
            ('Dawit Bekele', 'Executive Chef', False),
            ('Helen Girma', 'Front Office Manager', False),
            ('Tewodros Haile', 'Conference Services Manager', False),
        ]
        for i, (name, position, is_mgmt) in enumerate(team):
            TeamMember.objects.get_or_create(
                name=name,
                defaults={
                    'position': position, 'is_management': is_mgmt,
                    'bio': f'{name} brings years of hospitality experience to Arba Minch Tourist Hotel.',
                    'is_published': True, 'order': i,
                },
            )
