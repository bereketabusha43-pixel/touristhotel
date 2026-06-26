"""Gallery app admin."""
from django.contrib import admin

from core.admin_utils import image_preview
from gallery.models import GalleryCategory, GalleryImage


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 3
    fields = ('title', 'image', 'caption', 'is_published', 'order')


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'is_published', 'order', 'image_count')
    list_editable = ('is_published', 'order')
    list_filter = ('category_type',)
    inlines = [GalleryImageInline]

    @admin.display(description='Images')
    def image_count(self, obj):
        return obj.images.count()


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'is_featured', 'order', 'preview')
    list_editable = ('is_published', 'is_featured', 'order')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'caption')

    @admin.display(description='Preview')
    def preview(self, obj):
        return image_preview(obj)
