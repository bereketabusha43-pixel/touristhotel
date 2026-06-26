"""Template tags for hotel image helpers."""
from django import template
from django.templatetags.static import static

register = template.Library()

VIP_CATEGORIES = frozenset({'executive', 'family_suite', 'presidential'})


@register.simple_tag
def room_fallback_image(room) -> str:
    """Return static URL for room card fallback image."""
    if room.category.category_type in VIP_CATEGORIES:
        return static('images/vip-room.jpg')
    return static('images/rooms.jpg')
