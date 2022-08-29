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
