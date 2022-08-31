from django.urls import path
from . import api

urlpatterns = [
    path('', api.HotelListCreatedView.as_view(), name='hotel_list'),
    path('<slug:slug>/', api.HotelDetailView.as_view(), name='hotel_detail'),
    path('r/rooms/', api.RoomListCreateView.as_view(), name='rooms'),  # prefix r to prevent conflict with hotel details
    path('<slug:hotel_slug>/rooms/', api.RoomListByHotelView.as_view(), name='room_by_hotel'),
    path('rooms/<int:room_pk>/gallery/', api.RoomGalleryView.as_view(), name='room_gallery'),
    path('<int:hotel_pk>/gallery/', api.HotelGalleryView.as_view(), name='hotel_gallery'),
    path('r/rooms/<uuid:uuid>/', api.RoomDetailView.as_view(), name='room_detail')
]
