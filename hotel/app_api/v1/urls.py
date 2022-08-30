from django.urls import path
from . import api

urlpatterns = [
    path('', api.HotelListCreatedView.as_view(), name='hotel_list'),
    path('<int:hotel_pk>/gallery/', api.HotelGalleryView.as_view(), name='hotel_gallery'),
    path('<int:pk>/', api.HotelDetailView.as_view(), name='hotel_detail'),
    path('rooms/', api.RoomListCreateView.as_view(), name='rooms'),
    path('<int:hotel_pk>/rooms/', api.RoomListByHotelView.as_view(), name='room_by_hotel'),
    path('rooms/<int:room_pk>/gallery/', api.RoomGalleryView.as_view(), name='room_gallery')
]
