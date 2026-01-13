from .views import *
from rest_framework import routers
from django.urls import path, include

router = routers.SimpleRouter()
router.register(r'review', ReviewViewSet, basename='review')
router.register(r'booking', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
    path('booking', HotelListApiView.as_view(), name='hotel_list'),
    path('review_list/', ReviewListAPIView.as_view(), name='review_list'),
    path('booking<int:pk>/', HotelDetailApiView.as_view(), name='hotel_detail'),
    path('rooms/', RoomListApiView.as_view(), name='room_list'),
    path('rooms/<int:pk>', RoomDetailApiView.as_view(), name='room_detail'),
    path('rooms/create/', RoomCreateApiView.as_view(), name='room_create'),
    path('rooms/create/<int:pk>', RoomEditApiView.as_view(), name='room_edit'),
    path('country/', CountryApiView.as_view(), name='country_list'),
    path('country/<int:pk>', CountryDetailApiView.as_view(), name='country_detail'),
    path('user/', OwnerListApiView.as_view(), name='user_list'),
    path('user/<int:pk>', OwnerDetailApiView.as_view(), name='user_detail'),
    path('hotel/create/', HotelCreateApiView.as_view(), name='hotel_create'),
    path('hotel/create/<int:pk>', HotelEditApiView.as_view(), name='hotel_edit'),
    path('register/owner/', OwnerRegisterView.as_view(), name='register_owner'),
    path('register/client/', ClientRegisterView.as_view(), name='register_client'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
