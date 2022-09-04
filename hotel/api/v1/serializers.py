from rest_framework import serializers
from .models import Hotel, Location, Gallery, Room, Reservation
from django.utils import timezone


class GalleryRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        return value.image.url


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class HotelSerializer(serializers.ModelSerializer):
    gallery = GalleryRelatedField(many=True, read_only=True)
    location = LocationSerializer()
    host = serializers.CharField(source='host.username', read_only=True)
    url = serializers.URLField(read_only=True, source='get_absolute_url')

    class Meta:
        model = Hotel
        fields = '__all__'
        read_only_fields = ['host', 'is_active', 'gallery', 'slug']

    def create(self, validated_data):
        location = Location.objects.create(**validated_data.pop('location'))

        hotel = Hotel.objects.create(location=location, **validated_data)

        return hotel


class HotelMiniSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    host = serializers.CharField(source='host.username')

    class Meta:
        model = Hotel
        fields = '__all__'


class GallerySerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(), write_only=True, required=False)

    class Meta:
        model = Gallery
        fields = ['image', 'images']

    def create(self, validated_data):

        if validated_data.get('hotel_pk'):
            content_object = self._get_object_or_validation_error(
                Hotel, validated_data.pop('hotel_pk')
            )

        else:
            content_object = self._get_object_or_validation_error(
                Room, validated_data.pop('room_pk')
            )

        gallery = Gallery.objects.create(image=validated_data.get('image'),
                                         content_object=content_object)

        if validated_data.get('images', None):
            galleries = [Gallery(image=image, content_object=content_object)
                         for image in validated_data['images']]

            Gallery.objects.bulk_create(gallery)
            return galleries

        return gallery

    @staticmethod
    def _get_object_or_validation_error(model, pk):
        try:
            content_object = model.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise serializers.ValidationError('room not found')

        return content_object


class RoomWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['uuid']

    def validate(self, data):
        if self.context['request'].user.id != data['hotel'].host_id:
            raise serializers.ValidationError('you are not the hotel host')

        return data


class RoomReadSerializer(serializers.ModelSerializer):
    hotel = HotelMiniSerializer(read_only=True)
    url = serializers.URLField(read_only=True, source='get_absolute_url')
    gallery = GalleryRelatedField(read_only=True, many=True)

    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['uuid']


class ReservationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['guest', 'is_refund', 'uuid']

    def validate(self, data):
        room: Room = data.get('room')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date:
            if start_date < timezone.now().date() or end_date <= start_date:
                raise serializers.ValidationError('enter valid dates.')

        if room:
            for reservation in room.reservations.filter(is_canceled=False).values('start_date', 'end_date'):

                if start_date <= reservation['end_date'] \
                        and reservation['start_date'] <= end_date:
                    raise serializers.ValidationError('room is reserved already')

        return super().validate(data)


class RoomMiniSerializer(serializers.ModelSerializer):
    gallery = GalleryRelatedField(read_only=True, many=True)

    class Meta:
        model = Room
        fields = '__all__'


class ReservationReadSerializer(serializers.ModelSerializer):
    room = RoomMiniSerializer(read_only=True)
    url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['guest', 'is_refund', 'is_canceled', 'url']
