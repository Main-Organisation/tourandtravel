from django.urls import path
from .views import HotelView, RoomView, RoomAdditionalDetailsView


urlpatterns = [
    path('add-hotel', HotelView.as_view(), name='add-hotel'),
    path('add-room', RoomView.as_view(), name='add-room'),
    path('update-room', RoomAdditionalDetailsView.as_view(), name='update-room'),
]