from django.contrib import admin
from django.urls import path
from auto.views import catalogo, prenota, calendario, api_calendario

from django.contrib.auth import views as auth_views
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

path(
    "login/",
    auth_views.LoginView.as_view(
        template_name="login.html"
    ),
    name="login"
),

path(
    "logout/",
    auth_views.LogoutView.as_view(
        template_name="logout.html"
    ),
    name="logout"
),
]


if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )