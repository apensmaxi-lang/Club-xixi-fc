from django.contrib import admin

from .models import Jugador


@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ("dorsal", "nombre", "apellido", "edad", "altura_cm", "peso_kg", "posicion", "pierna_buena")
    list_filter = ("posicion", "pierna_buena")
    search_fields = ("nombre", "apellido")
    ordering = ("dorsal",)
