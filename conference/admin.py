"""Conference and events admin."""
from django.contrib import admin

from core.admin_utils import image_preview
from conference.models import ConferenceBooking, ConferenceHall, EventInquiry, EventPackage


@admin.register(ConferenceHall)
class ConferenceHallAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'price_per_day', 'is_published', 'is_featured', 'preview')
    list_editable = ('is_published', 'is_featured')
    list_filter = ('is_published',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    @admin.display(description='Image')
    def preview(self, obj):
        return image_preview(obj, 'main_image')


@admin.register(ConferenceBooking)
class ConferenceBookingAdmin(admin.ModelAdmin):
    list_display = ('organization', 'hall', 'event_date', 'attendees', 'status', 'created_at')
    list_filter = ('status', 'event_date')
    search_fields = ('organization', 'contact_name', 'email')
    list_editable = ('status',)


@admin.register(EventPackage)
class EventPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'price', 'max_guests', 'is_published', 'is_featured')
    list_editable = ('is_published', 'is_featured')
    list_filter = ('event_type', 'is_published')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(EventInquiry)
class EventInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'event_date', 'guests', 'is_read', 'created_at')
    list_filter = ('is_read', 'event_type')
    list_editable = ('is_read',)
    search_fields = ('name', 'email', 'message')
