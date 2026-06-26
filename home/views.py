"""Homepage and static page views."""
from django.views.generic import DetailView, ListView, TemplateView

from blog.models import BlogPost
from core.models import (
    Award,
    FAQ,
    HeroSlider,
    HomeFeature,
    SpecialOffer,
    TeamMember,
    Testimonial,
    TourPackage,
)
from gallery.models import GalleryImage
from rooms.models import Room


class HomeView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'hero_slides': HeroSlider.objects.filter(is_published=True),
            'features': HomeFeature.objects.filter(is_published=True)[:8],
            'featured_rooms': Room.objects.filter(is_published=True, is_featured=True)[:4],
            'testimonials': Testimonial.objects.filter(is_published=True, is_featured=True)[:6],
            'offers': SpecialOffer.objects.filter(is_published=True)[:3],
            'latest_posts': BlogPost.objects.filter(is_published=True)[:3],
            'awards': Award.objects.all()[:6],
            'gallery_images': GalleryImage.objects.filter(is_published=True, is_featured=True)[:8],
            'tour_packages': TourPackage.objects.filter(is_published=True, is_featured=True)[:4],
        })
        return ctx


class AboutView(TemplateView):
    template_name = 'home/about.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'team_members': TeamMember.objects.filter(is_published=True),
            'management': TeamMember.objects.filter(is_published=True, is_management=True),
            'awards': Award.objects.all(),
            'faqs': FAQ.objects.filter(is_published=True, category='general')[:10],
        })
        return ctx


class ExperienceListView(ListView):
    model = TourPackage
    template_name = 'home/experiences.html'
    context_object_name = 'tours'
    paginate_by = 9

    def get_queryset(self):
        return TourPackage.objects.filter(is_published=True)


class ExperienceDetailView(DetailView):
    model = TourPackage
    template_name = 'home/experience_detail.html'
    context_object_name = 'tour'
    slug_field = 'slug'


class OfferDetailView(DetailView):
    model = SpecialOffer
    template_name = 'home/offer_detail.html'
    context_object_name = 'offer'
    slug_field = 'slug'
