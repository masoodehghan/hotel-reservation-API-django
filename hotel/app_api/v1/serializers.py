from rest_framework import serializers
from ...models import Hotel, Location, Gallery


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

    class Meta:
        model = Hotel
        fields = '__all__'
        read_only_fields = ['host', 'is_active', 'gallery']

    def create(self, validated_data):
        # print(validated_data['location'])
        location = Location.objects.create(**validated_data.pop('location'))

        hotel = Hotel.objects.create(location=location, **validated_data)

        return hotel


class GallerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Gallery
        fields = ['image']

    def create(self, validated_data):
        try:
            hotel = Hotel.objects.get(pk=validated_data.pop('hotel_pk', None))
        except Hotel.DoesNotExist:
            raise serializers.ValidationError('hotel not found')

        gallery = Gallery.objects.create(image=validated_data.get('image'), content_object=hotel)

        return gallery
