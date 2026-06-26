"""Shared admin utilities."""
from django.utils.html import format_html


def image_preview(obj, field_name: str = 'image', width: int = 80) -> str:
    """Render a small image preview in Django admin."""
    image = getattr(obj, field_name, None)
    if image:
        return format_html('<img src="{}" width="{}" style="border-radius:4px;" />', image.url, width)
    return '—'
