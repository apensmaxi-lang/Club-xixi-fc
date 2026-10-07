from django.core.management.base import BaseCommand

from jugadoresapp.models import Jugador

# (nombre, apellido, dorsal, edad, altura_cm, peso_kg, posicion, pierna_buena)
DATOS = [
    ("Matías", "Fernández", 9, 27, 178, "74.5", "DELANTERO", "DERECHA"),
    ("Diego", "Rojas", 8, 25, 175, "70.0", "MEDIOCAMPISTA", "IZQUIERDA"),
    ("Sebastián", "Muñoz", 4, 30, 183, "80.2", "DEFENSA", "DERECHA"),
    ("Nicolás", "Vargas", 1, 28, 190, "85.0", "PORTERO", "DERECHA"),
    ("Felipe", "Soto", 11, 23, 172, "68.3", "DELANTERO", "AMBIDIESTRO"),
]


class Command(BaseCommand):
    help = "Carga jugadores de ejemplo en la base de datos."

    def handle(self, *args, **options):
        creados = 0
        for nombre, apellido, dorsal, edad, altura, peso, posicion, pierna in DATOS:
            _, nuevo = Jugador.objects.get_or_create(
                dorsal=dorsal,
                defaults=dict(nombre=nombre, apellido=apellido, edad=edad, altura_cm=altura,
                              peso_kg=peso, posicion=posicion, pierna_buena=pierna),
            )
            creados += nuevo
        self.stdout.write(self.style.SUCCESS(f"{creados} jugadores creados."))
