from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view as get_openapi_schema_view
from drf_yasg.views import get_schema_view as get_drf_yasg_schema_view
from drf_yasg import openapi
from rest_framework import permissions

yasg_schema_view = get_drf_yasg_schema_view(openapi.Info(
      title="PUT API YASG",
      default_version='v1',
   ),
   public=True, permission_classes=(permissions.AllowAny,),)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('api/', include('api.urls')),
    path('search/', include('search.urls')),
    path('openapi/', get_openapi_schema_view(
        title="Your Project",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),
    path(r'^swagger(?P<format>\.json|\.yaml)$',
        yasg_schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', yasg_schema_view.with_ui('swagger',
        cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', yasg_schema_view.with_ui('redoc',
        cache_timeout=0), name='schema-redoc'),
]
