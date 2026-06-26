from django.urls import path

from rooms import views

app_name = 'rooms'

urlpatterns = [
    path('', views.RoomListView.as_view(), name='list'),
    path('availability/', views.RoomAvailabilityView.as_view(), name='availability'),
    path('compare/', views.RoomCompareView.as_view(), name='compare'),
    path('<slug:slug>/', views.RoomDetailView.as_view(), name='detail'),
]
