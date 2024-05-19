from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Hotel, HotelImage, HotelVideo, Room, RoomAmenities, RoomBedType, RoomImage
from supplier.models import Supplier


class HotelView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'service/hotel.html')
    
    def post(self, request, *args, **kwargs):
        supplier = request.user.supplier
        # get all data from request
        name = request.POST.get('hotel_name')
        address = request.POST.get('hotel_address')
        contact = request.POST.get('hotel_contact')
        rooms = request.POST.get('rooms')
        policy = request.POST.get('policy')
        photos = request.FILES.getlist('photos')
        videos = request.FILES.getlist('videos')

        try:
            # create hotel
            hotel = Hotel.objects.create(
                supplier=supplier,
                name=name,
                address=address,
                contact_number=contact,
                policy=policy,
                rooms=int(rooms)
            )

            if photos:
                for photo in photos:
                    hotel_img = HotelImage.objects.create(
                        image=photo
                    )
                    hotel.hotel_images.add(hotel_img)
            if videos:
                for video in videos:
                    hotel_video = HotelVideo.objects.create(
                        video=video
                    )
                    hotel.hotel_videos.add(hotel_video)
            request.session['hotel_id'] = hotel.id
            messages.success(request, _('Hotel added successfully'))
            return redirect('add-room')
        except Exception as e:
            messages.error(request, _(str(e)))
            return redirect('supplier-dashboard')
        

class RoomView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'service/roomdetails.html')
    
    def post(self, request, *args, **kwargs):
        hotel_id = request.session.get('hotel_id')
        if not hotel_id:
            messages.error(request, _('Please add hotel first'))
            return redirect('supplier-dashboard')
        
        try:
            hotel = Hotel.objects.get(id=hotel_id)
        except Hotel.DoesNotExist:
            messages.error(request, _('Hotel does not exist'))
            return redirect('supplier-dashboard')
        
        # get all data from request
        category = request.POST.get('category')
        size = request.POST.get('size')
        bed_type = request.POST.get('bed_type')
        amenities = request.POST.get('amenities')
        room_photos = request.FILES.getlist('room_photos')

        try:
            room = Room.objects.create(
                hotel=hotel,
                room_size=size,
                category=category,
            )
            if bed_type:
                bed_type = RoomBedType.objects.create(bed_type=bed_type)
                room.bed_type.add(bed_type)
            if amenities:
                amenities_list = [amenity.strip() for amenity in amenities.split(',') if amenity.strip()]
                for amenity in amenities_list:
                    room_amenity = RoomAmenities.objects.create(name=amenity)
                    room.amenities.add(room_amenity)
            if room_photos:
                for photo in room_photos:
                    room_image = RoomImage.objects.create(
                        image=photo
                    )
                    room.room_images.add(room_image)
            request.session['room_id'] = room.id
            messages.success(request, _('Room added successfully'))
            return redirect('update-room')
        except Exception as e:
            messages.error(request, _(str(e)))
            return redirect('supplier-dashboard')
        

class RoomAdditionalDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'service/room_update.html')
    
    def post(self, request, *args, **kwargs):
        room_id = request.session.get('room_id')
        if not room_id:
            messages.error(request, _('Please add room first'))
            return redirect('supplier-dashboard')
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            messages.error(request, _('Room does not exist'))
            return redirect('supplier-dashboard')
        
        meal_plan = request.POST.get('meal_plan')
        single_price = request.POST.get('single_price')
        double_price = request.POST.get('double_price')
        extra_bed_price = request.POST.get('extra_bed_price')
        child_bed_price = request.POST.get('child_bed_price')
        no_child_bed_price = request.POST.get('no_child_bed_price')
        cancel_policy = request.POST.get('cancel_policy')
        num_guests = request.POST.get('num_guests')

        try:
            #update room with additional details
            room.meal_plan = meal_plan
            room.single = single_price
            room.double = double_price
            room.extra_bed = extra_bed_price
            room.child_bed = child_bed_price
            room.child_no_bed = no_child_bed_price
            room.number_of_guest = num_guests
            room.cancellation_policy = cancel_policy
            room.save()
            messages.success(request, _('Room updated with all details'))
            return redirect('supplier-dashboard')
        except Exception as e:
            messages.error(request, _(str(e)))
            return redirect('supplier-dashboard')

