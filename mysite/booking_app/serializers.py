from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class OwnerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'owner_role', 'age', 'phone_number']
        extra_kwargs={'password':{'write_only':True}}

    def create(self, validated_data):
        user=Owner.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }


class ClientRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'client_role', 'age', 'phone_number']
        extra_kwargs={'password':{'write_only':True}}

    def create(self, validated_data):
        user=Client.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }


class LoginSerializers(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)

    def validate(self, data):
        user=authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh=RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        self.token = data['refresh']
        return data

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except Exception as e:
            raise serializers.ValidationError({'detail': 'Недействительный или уже отозванный токен'})

class ClientSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name']

class OwnerSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['first_name', 'last_name']

class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['hotel_image']

class HotelServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelService
        fields = ['service']

class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = '__all__'

class RoomListSerializer(serializers.ModelSerializer):
    owner = OwnerSimpleSerializer()
    class Meta:
        model = Room
        fields = ['id', 'owner', 'number_room', 'room_type', 'room_status', 'price', 'room_image']

class RoomSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['number_room', 'room_type', 'room_status', 'price', 'room_image']


class RoomDetailSerializer(serializers.ModelSerializer):
    all_room_images = RoomImageSerializer(many=True, read_only=True)
    class Meta:
        model = Room
        fields = ['number_room', 'room_type', 'room_status', 'price', 'quantity_room',
                  'room_description', 'room_image', 'all_room_images']

class RoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class HotelSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['hotel_name']


class ReviewSerializer(serializers.ModelSerializer):
    username = ClientSimpleSerializer()
    hotel = HotelSimpleSerializer()
    class Meta:
        model = Review
        fields = ['username', 'hotel', 'text', 'stars']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class HotelListSerializer(serializers.ModelSerializer):
    hotel_image = HotelImageSerializer(many=True, read_only=True)
    get_avg_rating = serializers.SerializerMethodField()
    class Meta:
        model = Hotel
        fields = ['id', 'hotel_name', 'hotel_image', 'address', 'get_avg_rating']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

class HotelDetailSerializer(serializers.ModelSerializer):
    all_image_hotel = HotelImageSerializer(many=True, read_only=True)
    hotel_image = HotelImageSerializer(many=True, read_only=True)
    owner = OwnerSimpleSerializer()
    created_date = serializers.DateField(format('%d-%m-%Y'))
    rooms = RoomSimpleSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    hotel_service = HotelServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = ['hotel_name', 'description','country_name', 'address',
                  'hotel_image', 'all_image_hotel', 'created_date', 'owner', 'rooms', 'hotel_service', 'reviews']


class HotelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name']


class CountryDetailSerializer(serializers.ModelSerializer):
    country_hotel = HotelListSerializer(many=True, read_only=True)
    class Meta:
        model = Country
        fields = ['country_name', 'country_hotel']

