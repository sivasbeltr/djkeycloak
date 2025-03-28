from django.contrib import admin
from django.urls import include, path

from ornekapp.views import handler403, handler404, handler500

urlpatterns = [
    path("admin/", admin.site.urls),
    path("oidc/", include("mozilla_django_oidc.urls")),  # OIDC URL'leri
    path("", include("ornekapp.urls")),
]

# Özel hata işleyicileri
handler403 = "ornekapp.views.handler403"
handler404 = "ornekapp.views.handler404"
handler500 = "ornekapp.views.handler500"
