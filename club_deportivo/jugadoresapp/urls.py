from django.urls import path

from . import views

app_name = "jugadoresapp"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("jugadores/", views.lista, name="lista"),
    path("jugadores/nuevo/", views.crear, name="crear"),
    path("jugadores/<int:pk>/", views.detalle, name="detalle"),
    path("jugadores/<int:pk>/editar/", views.editar, name="editar"),
    path("jugadores/<int:pk>/eliminar/", views.eliminar, name="eliminar"),
]
