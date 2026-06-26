"""Room listing, detail, and comparison views."""
from django.db.models import Q
from django.views.generic import DetailView, ListView, TemplateView

from booking.forms import AvailabilitySearchForm
from booking.services import BookingService
from rooms.forms import RoomSearchForm
from rooms.models import Room, RoomCategory


class RoomListView(ListView):
    model = Room
    template_name = 'rooms/list.html'
    context_object_name = 'rooms'
    paginate_by = 12

    def get_queryset(self):
        qs = Room.objects.filter(is_published=True).select_related('category').prefetch_related('amenities')
        form = RoomSearchForm(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data
            if data.get('q'):
                qs = qs.filter(
                    Q(name__icontains=data['q']) | Q(description__icontains=data['q'])
                )
            if data.get('category'):
                qs = qs.filter(category=data['category'])
            if data.get('min_price'):
                qs = qs.filter(price_per_night__gte=data['min_price'])
            if data.get('max_price'):
                qs = qs.filter(price_per_night__lte=data['max_price'])
            if data.get('bed_type'):
                qs = qs.filter(bed_type=data['bed_type'])
            if data.get('lake_view'):
                qs = qs.filter(has_lake_view=True)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = RoomSearchForm(self.request.GET)
        ctx['categories'] = RoomCategory.objects.all()
        return ctx


class RoomDetailView(DetailView):
    model = Room
    template_name = 'rooms/detail.html'
    context_object_name = 'room'
    slug_field = 'slug'

    def get_queryset(self):
        return Room.objects.filter(is_published=True).prefetch_related('amenities', 'images')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['related_rooms'] = Room.objects.filter(
            is_published=True, category=self.object.category
        ).exclude(pk=self.object.pk)[:3]
        return ctx


class RoomCompareView(TemplateView):
    template_name = 'rooms/compare.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        slugs = self.request.GET.getlist('room')
        ctx['rooms'] = Room.objects.filter(slug__in=slugs, is_published=True).prefetch_related('amenities')
        return ctx


class RoomAvailabilityView(ListView):
    model = Room
    template_name = 'rooms/availability.html'
    context_object_name = 'rooms'
    paginate_by = 12

    def get_queryset(self):
        form = AvailabilitySearchForm(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data
            return BookingService.get_available_rooms(
                data['check_in'], data['check_out'],
                data['adults'], data.get('children', 0), data.get('num_rooms', 1),
            )
        return Room.objects.none()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = AvailabilitySearchForm(self.request.GET)
        return ctx
