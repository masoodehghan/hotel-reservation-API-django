from rest_framework import generics, permissions
from .serializers import (
    HotelSerializer,  GallerySerializer, RoomReadSerializer,
    RoomWriteSerializer
)
from ...models import Hotel, Location, Room, Gallery
from .permissions import IsHostOrReadOnly, IsGalleryHost, IsRoomHost


class HotelListCreatedView(generics.ListCreateAPIView):
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Hotel.objects.select_related('location').order_by('-id')
        return queryset

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)


class HotelGalleryView(generics.CreateAPIView):
    serializer_class = GallerySerializer
    permission_classes = [IsGalleryHost]
    queryset = Gallery.objects.all()

    def perform_create(self, serializer):
        serializer.save(hotel_pk=self.kwargs['hotel_pk'])


class HotelDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HotelSerializer
    permission_classes = [IsHostOrReadOnly]

    def get_queryset(self):
        return Hotel.objects.prefetch_related('gallery').all()


class RoomListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsRoomHost]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RoomWriteSerializer
        else:
            return RoomReadSerializer

    def get_queryset(self):
        queryset = Room.objects.select_related('hotel', 'hotel__location')

        return queryset


class RoomListByHotelView(generics.ListAPIView):
    serializer_class = RoomReadSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Room.objects.select_related('hotel', 'hotel__location')

        return queryset


class RoomGalleryView(generics.CreateAPIView):
    serializer_class = GallerySerializer
    permission_classes = [IsGalleryHost]
    queryset = Gallery.objects.all()

    def perform_create(self, serializer):
        serializer.save(room_pk=self.kwargs['room_pk'])
