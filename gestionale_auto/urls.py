from django.contrib import admin
from django.urls import path
from auto.views import catalogo, prenota, calendario
from auto.views import calendario_eventi

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
    calendario_eventi,
    name="calendario_eventi"
),
]