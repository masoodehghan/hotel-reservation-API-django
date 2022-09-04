from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from .serializers import (
    HotelSerializer, GallerySerializer, RoomReadSerializer,
    RoomWriteSerializer, ReservationReadSerializer, ReservationWriteSerializer
)
from .models import Hotel, Room, Gallery, Reservation

from .permissions import (
    IsHostOrReadOnly, IsGalleryHost,
    IsRoomHostOrReadOnly, IsGuestOrReadOnly
)

from .filters import HotelFilterSet
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.exceptions import NotAcceptable


class HotelListCreatedView(generics.ListCreateAPIView):
    serializer_class = HotelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HotelFilterSet

    def get_queryset(self):
        queryset = Hotel.objects.select_related('location', 'host').prefetch_related('gallery')
        return queryset.order_by('-id')

    def perform_create(self, serializer):
        if self.request.user.role == get_user_model().Roles.GUEST:
            raise NotAcceptable('only users with host or admin role can create hotel')
        else:
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
    lookup_field = 'slug'

    def get_queryset(self):
        return Hotel.objects.prefetch_related('gallery').all()


class RoomListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsRoomHostOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RoomWriteSerializer
        else:
            return RoomReadSerializer

    def get_queryset(self):
        queryset = Room.objects.select_related('hotel', 'hotel__location',
                                               'hotel__host').prefetch_related('gallery')

        return queryset.order_by('-id')


class RoomListByHotelView(generics.ListAPIView):
    serializer_class = RoomReadSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Room.objects.select_related('hotel', 'hotel__location', 'hotel__host')

        return queryset.prefetch_related('gallery').filter(hotel__slug=self.kwargs['hotel_slug'])


class RoomGalleryView(generics.CreateAPIView):
    serializer_class = GallerySerializer
    permission_classes = [IsGalleryHost]
    queryset = Gallery.objects.all()

    def perform_create(self, serializer):
        serializer.save(room_pk=self.kwargs['room_pk'])


class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsRoomHostOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return RoomWriteSerializer
        else:
            return RoomReadSerializer

    lookup_field = 'uuid'

    def get_queryset(self):
        queryset = Room.objects.select_related('hotel__host', 'hotel__location')

        return queryset


class ReservationListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReservationWriteSerializer
        else:
            return ReservationReadSerializer

    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)

    def get_queryset(self):
        queryset = Reservation.objects.select_related('room', 'room__hotel')

        return queryset.prefetch_related('room__gallery').filter(guest=self.request.user)


class ReservationDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ReservationWriteSerializer
        else:
            return ReservationReadSerializer

    permission_classes = [IsGuestOrReadOnly]
    lookup_field = 'uuid'

    def get_queryset(self):
        return Reservation.objects.all()
