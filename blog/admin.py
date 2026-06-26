"""Blog app admin."""
from django.contrib import admin

from core.admin_utils import image_preview
from blog.models import BlogCategory, BlogPost


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'is_published', 'order', 'post_count')
    list_editable = ('is_published', 'order')
    prepopulated_fields = {'slug': ('name',)}

    @admin.display(description='Posts')
    def post_count(self, obj):
        return obj.posts.count()


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'published_at', 'views', 'is_published', 'is_featured', 'preview')
    list_editable = ('is_published', 'is_featured')
    list_filter = ('category', 'is_published', 'published_at')
    search_fields = ('title', 'content', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    readonly_fields = ('views', 'created_at', 'updated_at')

    @admin.display(description='Image')
    def preview(self, obj):
        return image_preview(obj, 'featured_image')
