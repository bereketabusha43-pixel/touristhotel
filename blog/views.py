"""Blog views."""
from django.db.models import Q
from django.views.generic import DetailView, ListView

from blog.forms import BlogSearchForm
from blog.models import BlogPost


class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        qs = BlogPost.objects.filter(is_published=True).select_related('category')
        form = BlogSearchForm(self.request.GET)
        if form.is_valid():
            if q := form.cleaned_data.get('q'):
                qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(excerpt__icontains=q))
            if cat := form.cleaned_data.get('category'):
                qs = qs.filter(category=cat)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = BlogSearchForm(self.request.GET)
        return ctx


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    slug_field = 'slug'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).select_related('category')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        BlogPost.objects.filter(pk=obj.pk).update(views=obj.views + 1)
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['related_posts'] = BlogPost.objects.filter(
            is_published=True, category=self.object.category
        ).exclude(pk=self.object.pk)[:3]
        return ctx
