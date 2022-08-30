from rest_framework import generics, permissions
from .serializers import HotelSerializer, GallerySerializer
from ...models import Hotel, Location, Room, Gallery
from .permissions import IsHost


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
    permission_classes = [IsHost]
    queryset = Gallery.objects.all()

    def perform_create(self, serializer):
        serializer.save(hotel_pk=self.kwargs['hotel_pk'])
