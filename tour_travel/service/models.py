from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class HotelImage(models.Model):
    image = models.ImageField(upload_to='hotel_images', verbose_name=_('Hotel Image'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    # def __str__(self):
    #     return self.image.url

    class Meta:
        verbose_name = _('Hotel Image')
        verbose_name_plural = _('Hotel Images')


class HotelVideo(models.Model):
    video = models.FileField(upload_to='hotel_videos', verbose_name=_('Hotel Video'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    # def __str__(self):
    #     return self.video.url

    class Meta:
        verbose_name = _('Hotel Video')
        verbose_name_plural = _('Hotel Videos')


class Hotel(models.Model):
    supplier = models.ForeignKey('supplier.Supplier', on_delete=models.CASCADE, related_name='hotels')
    name = models.CharField(max_length=255, verbose_name=_('Hotel Name'))
    address = models.CharField(max_length=255, verbose_name=_('Hotel Address'), null=True, blank=True)
    policy = models.TextField(verbose_name=_('Hotel Policy'), null=True, blank=True)
    rooms = models.IntegerField(default=0, verbose_name=_('Hotel Rooms'))
    contact_number = models.CharField(max_length=15, verbose_name=_('Hotel Contact Number'), null=True, blank=True)
    hotel_images = models.ManyToManyField(HotelImage, blank=True)
    hotel_videos = models.ManyToManyField(HotelVideo, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Hotel')
        verbose_name_plural = _('Hotels')


class RoomBedType(models.Model):
    bed_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.bed_type


class RoomAmenities(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = _("Room Amenity")
        verbose_name_plural = _("Room Amenities")


class RoomImage(models.Model):
    image = models.ImageField(upload_to='room_images', verbose_name=_('Room Image'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.image.url

    class Meta:
        verbose_name = _('Room Image')
        verbose_name_plural = _('Room Images')


class Room(models.Model):
    ROOM_CATEGORY_CHOICES = (
        ('Delux', _('Delux')),
        ('Standerd', _('Standerd')),
        ('Suit', _('Suit')),
    )
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_rooms')
    room_size = models.CharField(max_length=55, null=True, blank=True)
    bed_type = models.ManyToManyField(RoomBedType, blank=True)
    amenities = models.ManyToManyField(RoomAmenities, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    room_images = models.ManyToManyField(RoomImage, blank=True)
    category = models.CharField(max_length=15, choices=ROOM_CATEGORY_CHOICES, default='Standerd')
    meal_plan = models.CharField(max_length=100, null=True, blank=True)

    # Net Price
    single = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text=_('Net Price single'))
    double = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text=_('Net Price double'))
    extra_bed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text=_('Extra Bed Adult'))
    child_bed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text=_('Extra Bed Child'))
    child_no_bed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text=_('No Bed Child'))
    number_of_guest = models.IntegerField(default=0)
    cancellation_policy = models.TextField(null=True, blank=True)

    # Booking status TODO: add booking status
    # is_booked = models.BooleanField(default=False)
    # checkin_date = models.DateField(null=True, blank=True)
    # checkout_date = models.DateField(null=True, blank=True)


    def __str__(self):
        return f"{self.hotel.name} - {self.room_size}"

    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')
