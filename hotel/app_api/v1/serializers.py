from rest_framework import serializers
from ...models import Hotel, Location


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = '__all__'


class HotelSerializer(serializers.ModelSerializer):

    location = LocationSerializer()

    class Meta:
        model = Hotel
        fields = '__all__'
        read_only_fields = ['host', 'is_active']

    def create(self, validated_data):
        # print(validated_data['location'])
        location = Location.objects.create(**validated_data.pop('location'))

        hotel = Hotel.objects.create(location=location, **validated_data)

        return hotel
