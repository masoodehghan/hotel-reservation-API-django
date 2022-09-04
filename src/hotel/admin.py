from django.contrib import admin
from hotel.api.v1.models import *

admin.site.register([Hotel, Reservation, Room])