from django import forms

from .models import Jugador

CAMPOS = ["nombre", "apellido", "dorsal", "edad", "altura_cm", "peso_kg", "posicion", "pierna_buena"]


class _JugadorBaseForm(forms.ModelForm):
    """Validaciones y estilos comunes a los formularios de crear y editar."""

    class Meta:
        model = Jugador
        fields = CAMPOS
        widgets = {
            "dorsal": forms.NumberInput(attrs={"min": 1, "max": 99}),
            "edad": forms.NumberInput(attrs={"min": 5, "max": 60}),
            "altura_cm": forms.NumberInput(attrs={"min": 100, "max": 230}),
            "peso_kg": forms.NumberInput(attrs={"min": 20, "max": 150, "step": "0.1"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            clase = "form-select" if isinstance(campo.widget, forms.Select) else "form-control"
            campo.widget.attrs["class"] = clase

    def clean_nombre(self):
        return self.cleaned_data["nombre"].strip().title()

    def clean_apellido(self):
        return self.cleaned_data["apellido"].strip().title()

    def clean_dorsal(self):
        dorsal = self.cleaned_data["dorsal"]
        repetido = Jugador.objects.filter(dorsal=dorsal)
        if self.instance.pk:
            repetido = repetido.exclude(pk=self.instance.pk)
        if repetido.exists():
            raise forms.ValidationError(f"El dorsal {dorsal} ya lo usa {repetido.first().nombre_completo}.")
        return dorsal


class JugadorCrearForm(_JugadorBaseForm):
    """Formulario de CREACIÓN (nuevo jugador)."""


class JugadorEditarForm(_JugadorBaseForm):
    """Formulario de EDICIÓN (jugador existente; el dorsal se valida ignorando al propio jugador)."""
