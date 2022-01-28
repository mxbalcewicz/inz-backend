from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('api/', include('api.urls')),
    path('search/', include('search.urls')),
    path('openapi/', get_schema_view(
        title="Your Project",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),
    path('spectacular/schema/', SpectacularAPIView.as_view(), name='schema'), # File response uri
    path('spectacular/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('spectacular/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
