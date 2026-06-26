from django.urls import path

from restaurant import views

app_name = 'restaurant'

urlpatterns = [
    path('', views.RestaurantView.as_view(), name='index'),
    path('reservation/', views.RestaurantReservationView.as_view(), name='reservation'),
]
