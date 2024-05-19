from django.contrib import admin
from .models import Hotel, HotelImage, HotelVideo, Room, RoomAmenities, RoomBedType, RoomImage

# Register your models here.


admin.site.register((Hotel, HotelImage, HotelVideo, Room, RoomAmenities, RoomBedType, RoomImage))