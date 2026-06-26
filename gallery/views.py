"""Gallery views."""
from django.views.generic import ListView

from gallery.models import GalleryCategory, GalleryImage


class GalleryListView(ListView):
    model = GalleryImage
    template_name = 'gallery/list.html'
    context_object_name = 'images'
    paginate_by = 20

    def get_queryset(self):
        qs = GalleryImage.objects.filter(is_published=True).select_related('category')
        category = self.request.GET.get('category')
        if category:
            qs = qs.filter(category__slug=category)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = GalleryCategory.objects.filter(is_published=True)
        ctx['active_category'] = self.request.GET.get('category', '')
        return ctx
