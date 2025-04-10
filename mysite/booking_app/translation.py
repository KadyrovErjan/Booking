from .models import Country, Hotel, Room, HotelService
from modeltranslation.translator import TranslationOptions,register


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('country_name',)


@register(Hotel)
class HotelTranslationOptions(TranslationOptions):
    fields = ('hotel_name', 'description', 'address',)


@register(HotelService)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('service', )


@register(Room)
class RoomTranslationOptions(TranslationOptions):
    fields = ('room_description',)