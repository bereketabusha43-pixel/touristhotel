from django.urls import path

from booking import views

app_name = 'booking'

urlpatterns = [
    path('', views.BookingSearchView.as_view(), name='search'),
    path('confirmation/<str:reference>/', views.BookingConfirmationView.as_view(), name='confirmation'),
    path('<slug:slug>/', views.BookingCreateView.as_view(), name='create'),
]
