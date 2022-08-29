from django.urls import path
from . import api

urlpatterns = [
    path('', api.HotelListCreatedView.as_view(), name='hotel_list')
]
