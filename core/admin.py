"""Core app admin configuration."""
from django.contrib import admin

from core.admin_utils import image_preview
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


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Hotel Information', {
            'fields': ('hotel_name', 'tagline', 'description', 'star_rating', 'logo', 'favicon'),
        }),
        ('Contact', {
            'fields': (
                'address', 'phone', 'phone_secondary', 'email', 'whatsapp', 'emergency_contact',
            ),
        }),
        ('Location', {
            'fields': ('google_maps_embed', 'latitude', 'longitude'),
        }),
        ('Operations', {
            'fields': ('business_hours', 'check_in_time', 'check_out_time'),
        }),
        ('About Page', {
            'fields': ('about_history', 'about_mission', 'about_vision', 'about_csr', 'why_choose_us'),
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('platform', 'is_active')


@admin.register(HeroSlider)
class HeroSliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'is_featured', 'order', 'preview')
    list_editable = ('is_published', 'is_featured', 'order')
    list_filter = ('is_published',)

    @admin.display(description='Preview')
    def preview(self, obj):
        return image_preview(obj, 'image')


@admin.register(HomeFeature)
class HomeFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'is_published', 'order')
    list_editable = ('is_published', 'order')


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'organization', 'order')
    list_editable = ('order',)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'is_management', 'is_published', 'order', 'preview')
    list_editable = ('is_management', 'is_published', 'order')
    list_filter = ('is_management', 'is_published')

    @admin.display(description='Photo')
    def preview(self, obj):
        return image_preview(obj, 'photo')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'country', 'rating', 'is_featured', 'is_published', 'order')
    list_editable = ('is_featured', 'is_published', 'order')
    list_filter = ('rating', 'is_featured', 'country')
    search_fields = ('guest_name', 'content', 'country')


@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'offer_type', 'discount_percent', 'valid_until', 'is_published', 'is_featured')
    list_editable = ('is_published', 'is_featured')
    list_filter = ('offer_type', 'is_published')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

    @admin.display(description='Image')
    def preview(self, obj):
        return image_preview(obj)


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'price', 'location', 'is_published', 'is_featured')
    list_editable = ('is_published', 'is_featured')
    list_filter = ('is_published',)
    search_fields = ('title', 'description', 'location')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'is_published', 'order')
    list_editable = ('is_published', 'order')
    list_filter = ('category', 'is_published')
    search_fields = ('question', 'answer')
