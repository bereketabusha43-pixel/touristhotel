"""Contact page views."""
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from contact.forms import ContactForm, NewsletterForm
from contact.models import NewsletterSubscriber
from core.models import FAQ


class ContactView(CreateView):
    form_class = ContactForm
    template_name = 'contact/index.html'
    success_url = reverse_lazy('contact:index')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['faqs'] = FAQ.objects.filter(is_published=True)[:8]
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Thank you for your message. We will respond within 24 hours.')
        return super().form_valid(form)


class NewsletterSubscribeView(CreateView):
    form_class = NewsletterForm
    http_method_names = ['post']

    def form_valid(self, form):
        form.save()
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Successfully subscribed!'})
        messages.success(self.request, 'Successfully subscribed to our newsletter!')
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        messages.error(self.request, 'Subscription failed. Please check your email.')
        return super().form_invalid(form)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', reverse_lazy('home:index'))
