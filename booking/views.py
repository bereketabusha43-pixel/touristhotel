"""Booking views."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView

from booking.forms import AvailabilitySearchForm, BookingForm
from booking.models import Booking
from booking.services import BookingService
from rooms.models import Room


class BookingSearchView(TemplateView):
    template_name = 'booking/search.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = AvailabilitySearchForm(self.request.GET or None)
        ctx['search_form'] = form
        if form.is_valid():
            data = form.cleaned_data
            ctx['available_rooms'] = BookingService.get_available_rooms(
                data['check_in'], data['check_out'],
                data['adults'], data.get('children', 0), data.get('num_rooms', 1),
            )
        return ctx


class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking/create.html'

    def dispatch(self, request, *args, **kwargs):
        self.room = get_object_or_404(Room, slug=kwargs['slug'], is_published=True)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['room'] = self.room
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        for field in ('check_in', 'check_out', 'adults', 'children', 'num_rooms'):
            if val := self.request.GET.get(field):
                initial[field] = val
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['room'] = self.room
        return ctx

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, f'Booking confirmed! Reference: {self.object.reference}')
        return redirect('booking:confirmation', reference=self.object.reference)


class BookingConfirmationView(DetailView):
    model = Booking
    template_name = 'booking/confirmation.html'
    context_object_name = 'booking'
    slug_field = 'reference'
    slug_url_kwarg = 'reference'

    def get_queryset(self):
        return Booking.objects.select_related('guest', 'room', 'room__category')
