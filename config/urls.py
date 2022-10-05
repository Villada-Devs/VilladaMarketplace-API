from telnetlib import STATUS
from django import http
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.http import HttpResponse

schema_view = get_schema_view(
    openapi.Info(
        title="API DOCS",
        default_version='v1',
        description="Docs and api endpoints description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', lambda request: HttpResponse("https://www.youtube.com/watch?v=OqSQo2aifAA&ab_channel=AnabelaEspenan", content_type="text/plain"), name='healtchecker'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('apiauth.urls')),
    path('api/v1/', include('events.urls')),
    path('api/v1/marketplace/', include('marketplace.urls')),
    path('api/v1/', include('carpool.urls')),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

