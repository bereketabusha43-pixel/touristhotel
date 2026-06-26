"""Booking app admin."""
from django.contrib import admin
from django.utils.html import format_html

from booking.models import Booking, Guest


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'country', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'reference', 'guest', 'room', 'check_in', 'check_out', 'nights',
        'status_badge', 'payment_status', 'total_price', 'created_at',
    )
    list_filter = ('status', 'payment_status', 'check_in', 'created_at')
    search_fields = ('reference', 'guest__first_name', 'guest__last_name', 'guest__email')
    readonly_fields = ('reference', 'created_at', 'updated_at', 'confirmed_at')
    date_hierarchy = 'check_in'
    actions = ['confirm_bookings', 'cancel_bookings']

    fieldsets = (
        ('Booking Details', {
            'fields': ('reference', 'guest', 'room', 'status', 'payment_status'),
        }),
        ('Stay', {
            'fields': ('check_in', 'check_out', 'adults', 'children', 'num_rooms', 'total_price'),
        }),
        ('Notes', {
            'fields': ('special_requests', 'admin_notes'),
        }),
        ('Timestamps', {
            'fields': ('confirmed_at', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Status')
    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'confirmed': '#28a745',
            'checked_in': '#17a2b8',
            'checked_out': '#6c757d',
            'cancelled': '#dc3545',
            'no_show': '#343a40',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:4px;">{}</span>',
            color, obj.get_status_display(),
        )

    @admin.action(description='Confirm selected bookings')
    def confirm_bookings(self, request, queryset):
        for booking in queryset.filter(status='pending'):
            booking.confirm()
        self.message_user(request, f'{queryset.count()} booking(s) confirmed.')

    @admin.action(description='Cancel selected bookings')
    def cancel_bookings(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, f'{queryset.count()} booking(s) cancelled.')
