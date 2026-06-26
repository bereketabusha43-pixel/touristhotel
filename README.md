# Arba Minch Tourist Hotel Website

A production-grade Django hotel website for **Arba Minch Tourist Hotel** in Southern Ethiopia.

## Features

- **Luxury hotel website** with Bootstrap 5.3, mobile-first responsive design
- **Room management** with categories, amenities, gallery, search, and comparison
- **Booking system** with availability checking and confirmation
- **Restaurant** with menu and table reservations
- **Conference & Events** with inquiry forms and packages
- **Gallery** with categories, lightbox, and lazy loading
- **Blog** with categories, search, and SEO-friendly URLs
- **Experiences** tour packages for local attractions
- **Contact** form, newsletter, FAQs, and Google Maps placeholder
- **SEO optimized** with Schema.org, OpenGraph, sitemap, and robots.txt
- **Django Admin** with image previews, filters, bulk actions
- **Production ready** for PythonAnywhere deployment

## Tech Stack

- Python 3.13+ / Django 5+
- SQLite (development) / MySQL (production)
- Bootstrap 5.3, Vanilla JavaScript
- Pillow, django-environ, WhiteNoise, django-crispy-forms, django-filter, django-ckeditor

## Quick Start

### 1. Clone and setup

```bash
cd zebib
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Environment

```bash
copy .env.example .env
```

Edit `.env` and set your `SECRET_KEY`.

### 3. Database

```bash
python manage.py migrate
python manage.py populate_sample_data
python manage.py createsuperuser
```

### 4. Run development server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000

## Project Structure

```
zebib/
├── config/           # Django project settings
├── core/             # Site settings, testimonials, offers, tours
├── home/             # Homepage, about, experiences
├── rooms/            # Room models and views
├── booking/          # Reservation system
├── restaurant/       # Dining and menu
├── conference/       # Meetings and events
├── gallery/          # Photo gallery
├── blog/             # Articles and travel guides
├── contact/          # Contact form and newsletter
├── accounts/         # Future user accounts
├── templates/        # HTML templates with partials
├── static/           # CSS, JS, images
└── media/            # Uploaded files
```

## Admin

Access the admin at `/admin/` to manage:

- Site settings, hero sliders, features
- Rooms, amenities, and images
- Bookings and guest information
- Restaurant menu and reservations
- Conference halls and event packages
- Gallery, blog, testimonials, offers
- Contact messages and newsletter subscribers

## Deployment (PythonAnywhere)

**Full step-by-step guide:** see [DEPLOYMENT.md](DEPLOYMENT.md)

Quick summary:

1. Upload project to `/home/YOURUSERNAME/zebib`
2. `mkvirtualenv --python=/usr/bin/python3.10 amth-env`
3. `pip install -r requirements.txt`
4. `cp .env.production.example .env` and edit values
5. `python manage.py migrate && python manage.py collectstatic --noinput`
6. Configure WSGI from `scripts/pythonanywhere_wsgi.py`
7. Map `/media/` in Web tab static files
8. Reload web app

## Testing

```bash
python manage.py test
```

## Sample Data

The `populate_sample_data` command creates:

- 50 rooms across 7 categories
- 15 blog posts
- 40 gallery entries
- 20 testimonials
- 15 FAQs
- 10 special offers
- 20+ menu items
- 5 conference halls
- 5 tour packages

## Future Integrations

The project is structured for:

- Online payments (Chapa, Telebirr, Stripe)
- Google Maps API
- Email/SMS notifications
- User accounts and loyalty program
- Multilingual support (English/Amharic)
- Channel manager and CRM integration

## License

Proprietary — Arba Minch Tourist Hotel
