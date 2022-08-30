from rest_framework import generics, permissions
from .serializers import HotelSerializer
from ...models import Hotel, Location, Room, Gallery


class HotelListCreatedView(generics.ListCreateAPIView):
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Hotel.objects.select_related('location').order_by('-id')
        return queryset

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)
