"""Restaurant app admin."""
from django.contrib import admin

from core.admin_utils import image_preview
from restaurant.models import MenuCategory, MenuItem, Restaurant, RestaurantReservation


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Information', {'fields': ('name', 'description', 'main_image', 'chef_name', 'chef_special')}),
        ('Hours', {'fields': ('breakfast_hours', 'lunch_hours', 'dinner_hours')}),
    )

    def has_add_permission(self, request):
        return not Restaurant.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = ('name', 'price', 'is_vegetarian', 'is_spicy', 'is_chef_special', 'is_published', 'order')


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'is_published', 'order')
    list_editable = ('is_published', 'order')
    inlines = [MenuItemInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_vegetarian', 'is_chef_special', 'is_published', 'preview')
    list_editable = ('is_published',)
    list_filter = ('category', 'is_vegetarian', 'is_spicy', 'is_chef_special')
    search_fields = ('name', 'description')

    @admin.display(description='Image')
    def preview(self, obj):
        return image_preview(obj)


@admin.register(RestaurantReservation)
class RestaurantReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'guests', 'status', 'created_at')
    list_filter = ('status', 'date')
    search_fields = ('name', 'email', 'phone')
    list_editable = ('status',)
