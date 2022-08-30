from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/hotels/', include('hotel.app_api.v1.urls')),
    path('api/v1/accounts/', include('users.api.v1.urls'))
]
