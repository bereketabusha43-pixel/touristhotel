from django.urls import path

from home import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('experiences/', views.ExperienceListView.as_view(), name='experiences'),
    path('experiences/<slug:slug>/', views.ExperienceDetailView.as_view(), name='experience_detail'),
    path('offers/<slug:slug>/', views.OfferDetailView.as_view(), name='offer_detail'),
]
