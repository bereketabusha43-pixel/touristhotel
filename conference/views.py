"""Conference and events views."""
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from conference.forms import ConferenceBookingForm, EventInquiryForm
from conference.models import ConferenceHall, EventPackage


class ConferenceListView(ListView):
    model = ConferenceHall
    template_name = 'conference/index.html'
    context_object_name = 'halls'
    paginate_by = 6

    def get_queryset(self):
        return ConferenceHall.objects.filter(is_published=True)


class ConferenceDetailView(DetailView):
    model = ConferenceHall
    template_name = 'conference/detail.html'
    context_object_name = 'hall'
    slug_field = 'slug'


class ConferenceBookingView(CreateView):
    form_class = ConferenceBookingForm
    template_name = 'conference/booking.html'
    success_url = reverse_lazy('conference:index')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if slug := self.kwargs.get('slug'):
            ctx['hall'] = ConferenceHall.objects.filter(slug=slug).first()
        return ctx

    def form_valid(self, form):
        if slug := self.kwargs.get('slug'):
            form.instance.hall = get_object_or_404(ConferenceHall, slug=slug)
        elif not form.instance.hall_id:
            messages.error(self.request, 'Please select a conference hall.')
            return self.form_invalid(form)
        messages.success(self.request, 'Your conference inquiry has been submitted successfully.')
        return super().form_valid(form)


class EventsView(ListView):
    model = EventPackage
    template_name = 'conference/events.html'
    context_object_name = 'packages'
    paginate_by = 6

    def get_queryset(self):
        return EventPackage.objects.filter(is_published=True)


class EventDetailView(DetailView):
    model = EventPackage
    template_name = 'conference/event_detail.html'
    context_object_name = 'package'
    slug_field = 'slug'


class EventInquiryView(CreateView):
    form_class = EventInquiryForm
    template_name = 'conference/inquiry.html'
    success_url = reverse_lazy('conference:events')

    def form_valid(self, form):
        if slug := self.kwargs.get('slug'):
            try:
                form.instance.package = EventPackage.objects.get(slug=slug)
            except EventPackage.DoesNotExist:
                pass
        messages.success(self.request, 'Your event inquiry has been received. Our events team will contact you.')
        return super().form_valid(form)
