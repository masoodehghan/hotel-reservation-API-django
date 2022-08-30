from django.urls import path
from . import api

urlpatterns = [
    path('', api.HotelListCreatedView.as_view(), name='hotel_list'),
    path('<int:hotel_pk>/gallery/', api.HotelGalleryView.as_view(), name='hotel_gallery')
]
