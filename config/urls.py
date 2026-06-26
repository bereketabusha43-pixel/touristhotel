"""Main URL configuration."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from core.sitemaps import (
    BlogSitemap,
    ConferenceSitemap,
    EventSitemap,
    OfferSitemap,
    RoomSitemap,
    StaticViewSitemap,
    TourSitemap,
)
from core.views import robots_txt

sitemaps = {
    'static': StaticViewSitemap,
    'rooms': RoomSitemap,
    'blog': BlogSitemap,
    'conference': ConferenceSitemap,
    'events': EventSitemap,
    'tours': TourSitemap,
    'offers': OfferSitemap,
}

admin.site.site_header = 'Arba Minch Tourist Hotel Admin'
admin.site.site_title = 'AMTH Admin'
admin.site.index_title = 'Hotel Management Dashboard'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('robots.txt', robots_txt, name='robots'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('', include('home.urls')),
    path('rooms/', include('rooms.urls')),
    path('booking/', include('booking.urls')),
    path('dining/', include('restaurant.urls')),
    path('conference/', include('conference.urls')),
    path('gallery/', include('gallery.urls')),
    path('blog/', include('blog.urls')),
    path('contact/', include('contact.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
