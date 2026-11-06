from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/", include("jugadoresapp.api_urls")),
    path("admin/", admin.site.urls),
    path("", include("jugadoresapp.urls")),
]
