"""Contact app admin."""
from django.contrib import admin

from contact.models import ContactMessage, NewsletterSubscriber


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'is_replied', 'created_at')
    list_filter = ('subject', 'is_read', 'is_replied', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_editable = ('is_read', 'is_replied')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'confirmed', 'created_at')
    list_filter = ('is_active', 'confirmed')
    search_fields = ('email',)
    actions = ['deactivate_subscribers']

    @admin.action(description='Deactivate selected subscribers')
    def deactivate_subscribers(self, request, queryset):
        queryset.update(is_active=False)
