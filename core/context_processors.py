"""Context processors for global template variables."""
from typing import Any

from django.http import HttpRequest

from core.models import SiteSettings, SocialMedia


def site_settings(request: HttpRequest) -> dict[str, Any]:
    """Inject site-wide settings into every template."""
    settings_obj = SiteSettings.load()
    social_links = SocialMedia.objects.filter(is_active=True)
    return {
        'site_settings': settings_obj,
        'social_links': social_links,
    }
