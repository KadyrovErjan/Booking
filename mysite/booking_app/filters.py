from django_filters import FilterSet
from .models import Hotel, Room


class HotelFilter(FilterSet):
    class Meta:
        model = Hotel
        fields = {
            'country_name': ['exact'],
        }

class RoomFilter(FilterSet):
    class Meta:
        model = Room
        fields = {
            'number_room': ['gt', 'lt'],
            'price': ['gt', 'lt'],
            'quantity_room': ['gt', 'lt'],
            'room_status': ['exact']

        }

