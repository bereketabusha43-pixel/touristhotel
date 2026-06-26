from django.urls import path

from conference import views

app_name = 'conference'

urlpatterns = [
    path('', views.ConferenceListView.as_view(), name='index'),
    path('booking/', views.ConferenceBookingView.as_view(), name='booking'),
    path('booking/<slug:slug>/', views.ConferenceBookingView.as_view(), name='booking_hall'),
    path('events/', views.EventsView.as_view(), name='events'),
    path('events/inquiry/', views.EventInquiryView.as_view(), name='inquiry'),
    path('events/inquiry/<slug:slug>/', views.EventInquiryView.as_view(), name='inquiry_package'),
    path('events/<slug:slug>/', views.EventDetailView.as_view(), name='event_detail'),
    path('<slug:slug>/', views.ConferenceDetailView.as_view(), name='detail'),
]
