from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

PASSWORD = '12345'
HOTEL_URL = reverse('hotel_list')


class HotelTest(APITestCase):

    api_client = APIClient()

    @classmethod
    def setUpTestData(cls):
        cls.user, _ = get_user_model().objects.get_or_create(username='masood', password=PASSWORD)

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
