from django.urls import path

from contact import views

app_name = 'contact'

urlpatterns = [
    path('', views.ContactView.as_view(), name='index'),
    path('newsletter/', views.NewsletterSubscribeView.as_view(), name='newsletter'),
]
