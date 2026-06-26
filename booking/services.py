"""
Booking availability and pricing services.
"""
from datetime import date
from decimal import Decimal

from django.db.models import Q, QuerySet

from booking.models import Booking
from rooms.models import Room


class BookingService:
    """Service layer for room availability and booking operations."""

    @staticmethod
    def get_available_rooms(
        check_in: date,
        check_out: date,
        adults: int = 1,
        children: int = 0,
        num_rooms: int = 1,
    ) -> QuerySet[Room]:
        """Return rooms available for the given date range and guest count."""
        if check_out <= check_in:
            return Room.objects.none()

        booked_room_ids = Booking.objects.filter(
            status__in=['pending', 'confirmed', 'checked_in'],
            check_in__lt=check_out,
            check_out__gt=check_in,
        ).values_list('room_id', flat=True)

        total_guests = adults + children
        return (
            Room.objects.filter(is_published=True, availability_status='available')
            .exclude(id__in=booked_room_ids)
            .filter(max_occupancy__gte=total_guests)
            .filter(max_adults__gte=adults)
            .select_related('category')
            .prefetch_related('amenities', 'images')
            .distinct()
        )

    @staticmethod
    def is_room_available(room: Room, check_in: date, check_out: date) -> bool:
        """Check if a specific room is available for the date range."""
        if room.availability_status != 'available' or not room.is_published:
            return False
        if check_out <= check_in:
            return False
        return not Booking.objects.filter(
            room=room,
            status__in=['pending', 'confirmed', 'checked_in'],
            check_in__lt=check_out,
            check_out__gt=check_in,
        ).exists()

    @staticmethod
    def calculate_total(room: Room, check_in: date, check_out: date, num_rooms: int = 1) -> Decimal:
        """Calculate total price for a stay."""
        nights = (check_out - check_in).days
        return room.price_per_night * nights * num_rooms

    @staticmethod
    def search_rooms(
        queryset: QuerySet[Room],
        category: str | None = None,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
        bed_type: str | None = None,
        lake_view: bool | None = None,
        query: str | None = None,
    ) -> QuerySet[Room]:
        """Filter rooms by search criteria."""
        if category:
            queryset = queryset.filter(category__slug=category)
        if min_price is not None:
            queryset = queryset.filter(price_per_night__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price_per_night__lte=max_price)
        if bed_type:
            queryset = queryset.filter(bed_type=bed_type)
        if lake_view is not None:
            queryset = queryset.filter(has_lake_view=lake_view)
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(category__name__icontains=query)
            )
        return queryset
