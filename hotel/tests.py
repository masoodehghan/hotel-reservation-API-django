from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class HotelTest(APITestCase):

    def test_hotel_list(self):
        url = reverse('hotel_list')
        print(url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

