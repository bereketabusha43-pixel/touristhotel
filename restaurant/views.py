"""Restaurant page views."""
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from restaurant.forms import RestaurantReservationForm
from restaurant.models import MenuCategory, MenuItem, Restaurant


class RestaurantView(TemplateView):
    template_name = 'restaurant/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['restaurant'] = Restaurant.load()
        ctx['menu_categories'] = MenuCategory.objects.filter(is_published=True).prefetch_related('items')
        ctx['chef_specials'] = MenuItem.objects.filter(is_published=True, is_chef_special=True)[:6]
        return ctx


class RestaurantReservationView(CreateView):
    form_class = RestaurantReservationForm
    template_name = 'restaurant/reservation.html'
    success_url = reverse_lazy('restaurant:index')

    def form_valid(self, form):
        messages.success(self.request, 'Your table reservation has been submitted. We will confirm shortly.')
        return super().form_valid(form)
