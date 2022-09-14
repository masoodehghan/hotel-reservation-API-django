from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny


schema_view = get_schema_view(
    openapi.Info(
        title='Hotel Reservation API',
        default_version='v1',
    ),
    public=True,
    permission_classes=[AllowAny]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/hotels/', include('hotel.api.v1.urls')),
    path('api/v1/accounts/', include('users.api.v1.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('api/v1/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_schema'),
    path('api/v1/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='swagger_redoc'),
    path('api/v1/oauth/', include('drf_social_oauth2.urls', namespace='drf')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
