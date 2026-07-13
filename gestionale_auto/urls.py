from django.contrib import admin
from django.urls import path
from auto.views import catalogo, prenota, calendario, api_calendario

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('admin/', admin.site.urls),

    path(
        '',
        catalogo,
        name="catalogo"
    ),

    path(
        'prenota/<int:id_auto>/',
        prenota,
        name="prenota"
    ),

    path(
        'calendario/',
        calendario,
        name="calendario"
    ),

    path(
    'api/calendario/',
    api_calendario,
    name="api_calendario"
),

]


if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )