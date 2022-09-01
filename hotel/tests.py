from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from hotel.api.v1.models import Hotel, Location

PASSWORD = '12345'
HOTEL_URL = reverse('hotel_list')


class HotelTest(APITestCase):

    api_client = APIClient()

    @classmethod
    def setUpTestData(cls):
        cls.user, _ = get_user_model().objects.get_or_create(username='masood', password=PASSWORD)
        location = Location.objects.create(
            country='Test', city='Test City', district='test', street='test street'
        )

        cls.hotel = Hotel.objects.create(location=location, name='test name', host=cls.user)

    def test_hotel_list(self):
        response = self.client.get(HOTEL_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_hotel_create(self):
        data = {
            'location': {
                'country': 'Iran',
                'city': 'tehran',
                'district': 'test',
                'street': 'test_street'
            },
            'name': 'test_name'
        }

        self.api_client.force_authenticate(self.user)
        response = self.api_client.post(HOTEL_URL, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_hotel_detail(self):
        # url = reverse('hotel_detail', args=[self.hotel.pk])

        response = self.api_client.get(self.hotel.get_absolute_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['name'], self.hotel.name)

    def test_hotel_update(self):

        data = {'name': 'test update name'}
        self.api_client.force_authenticate(self.user)

        response = self.api_client.patch(self.hotel.get_absolute_url(), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.hotel.refresh_from_db()
        self.assertEqual(response.data['name'], data['name'])

    def test_room_list_by_hotel(self):
        url = reverse('room_by_hotel', args=[self.hotel.pk])

        res = self.api_client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
