from django.urls import path
from . import api_views

urlpatterns = [
    path("jugadores/", api_views.jugadores, name="api-jugadores"),
    path("jugadores/<int:pk>/", api_views.jugador, name="api-jugador"),
]
