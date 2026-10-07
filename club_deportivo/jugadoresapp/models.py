from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models

solo_letras = RegexValidator(
    regex=r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü' -]+$",
    message="Solo se permiten letras y espacios.",
)


class Jugador(models.Model):
    """Jugador del club. Campos: nombre, apellido, dorsal, edad, altura, peso,
    posición y pierna buena."""

    class Posicion(models.TextChoices):
        PORTERO = "PORTERO", "Portero"
        DEFENSA = "DEFENSA", "Defensa"
        MEDIO = "MEDIOCAMPISTA", "Mediocampista"
        DELANTERO = "DELANTERO", "Delantero"

    class Pierna(models.TextChoices):
        DERECHA = "DERECHA", "Derecha"
        IZQUIERDA = "IZQUIERDA", "Izquierda"
        AMBIDIESTRO = "AMBIDIESTRO", "Ambidiestro"

    nombre = models.CharField(max_length=50, validators=[solo_letras])
    apellido = models.CharField(max_length=50, validators=[solo_letras])
    dorsal = models.PositiveSmallIntegerField(
        unique=True,
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        help_text="Número entre 1 y 99, único en el club.",
    )
    edad = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(5), MaxValueValidator(60)],
        verbose_name="Edad (años)",
        help_text="Entre 5 y 60 años.",
    )
    altura_cm = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(100), MaxValueValidator(230)],
        verbose_name="Altura (cm)",
        help_text="Entre 100 y 230 cm.",
    )
    peso_kg = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        validators=[MinValueValidator(Decimal("20")), MaxValueValidator(150)],
        verbose_name="Peso (kg)",
        help_text="Entre 20 y 150 kg (puedes usar un decimal, ej. 72.5).",
    )
    posicion = models.CharField(max_length=20, choices=Posicion.choices, verbose_name="Posición")
    pierna_buena = models.CharField(max_length=12, choices=Pierna.choices, verbose_name="Pierna buena")

    class Meta:
        ordering = ["apellido", "nombre"]
        verbose_name_plural = "jugadoresapp"

    def __str__(self):
        return f"{self.nombre} {self.apellido} (#{self.dorsal})"

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
