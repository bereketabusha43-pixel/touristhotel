"""Rooms app admin."""
from django.contrib import admin

from core.admin_utils import image_preview
from rooms.models import Amenity, Room, RoomCategory, RoomImage


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1
    fields = ('image', 'caption', 'order', 'is_primary')


@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'order')
    list_editable = ('order',)
    search_fields = ('name',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'room_number', 'name', 'category', 'price_per_night', 'availability_status',
        'is_published', 'preview',
    )
    list_editable = ('availability_status', 'is_published')
    list_filter = ('category', 'availability_status', 'bed_type', 'is_published', 'has_lake_view')
    search_fields = ('name', 'room_number', 'description')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('amenities',)
    inlines = [RoomImageInline]
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'room_number', 'category', 'floor'),
        }),
        ('Details', {
            'fields': (
                'description', 'short_description', 'price_per_night', 'size_sqm',
                'bed_type', 'max_occupancy', 'max_adults', 'max_children',
            ),
        }),
        ('Features', {
            'fields': ('amenities', 'has_balcony', 'has_lake_view', 'policies'),
        }),
        ('Status & Media', {
            'fields': ('availability_status', 'main_image', 'is_published', 'is_featured', 'order'),
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Image')
    def preview(self, obj):
        return image_preview(obj, 'main_image')
