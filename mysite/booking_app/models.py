from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

ROLE_CHOICES = (
    ('owner', 'owner'),
    ('client', 'client')
)

class UserProfile(AbstractUser):
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='client')
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100),
                                                       MinValueValidator(18)], null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)


    def __str__(self):
        return f'{self.first_name}, {self.last_name}'



class Owner(UserProfile):
    owner_role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='owner')

    class Meta:
        verbose_name = 'Owner'


    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Client(UserProfile):
    client_role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='client')

    class Meta:
        verbose_name = 'Client'

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Country(models.Model):
    country_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.country_name

class Hotel(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=32)
    description = models.TextField()
    country_name = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country_hotel')
    address = models.CharField(max_length=64)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.hotel_name}, - {self.country_name}'

    def get_avg_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum([review.stars for review in reviews]) / reviews.count(), 1)
        return 0

class HotelService(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_service')
    service = models.CharField(max_length=64)

class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='all_image_hotel')
    hotel_image = models.ImageField(upload_to='hotel_image/')


class Room(models.Model):
    hotel_room = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    number_room = models.PositiveSmallIntegerField()
    TYPE_CHOICES = (
        ('люкс', 'люкс'),
        ('семейный', 'семейный'),
        ('одноместный', 'одноместный'),
        ('двухместный', 'двухместный')
    )
    room_type = models.CharField(max_length=16, choices=TYPE_CHOICES)
    STATUS_CHOICES = (
        ('свободен', 'свободен'),
        ('забронирован', 'забронирован'),
        ('занят', 'занят'),
    )
    room_status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='свободен')
    room_image = models.ImageField(upload_to='room_image')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_room = models.PositiveSmallIntegerField()
    room_description = models.TextField()
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.hotel_room}, - {self.number_room} - {self.room_type}'

class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='all_room_images')
    room_image = models.ImageField(upload_to='room_image/')

class Review(models.Model):
    username = models.ForeignKey(Client, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)

    def __str__(self):
        return f'{self.username}, - {self.hotel} - {self.stars}'

class Booking(models.Model):
    hotel_book = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_book = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.PositiveIntegerField(default=0)
    STATUS_BOOK_CHOICES = (
        ('отменено', 'отменено'),
        ('подтверждено', 'подтверждено'),
    )
    status_book = models.CharField(max_length=16, choices=STATUS_BOOK_CHOICES)

    def __str__(self):
        return f'{self.user}, - {self.hotel_book} - {self.room_book}, {self.status_book}'
