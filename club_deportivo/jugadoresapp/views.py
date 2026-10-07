from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import JugadorCrearForm, JugadorEditarForm
from .models import Jugador


ORDEN_LINEAS = [
    (Jugador.Posicion.DELANTERO, "Delanteros"),
    (Jugador.Posicion.MEDIO, "Mediocampistas"),
    (Jugador.Posicion.DEFENSA, "Defensas"),
    (Jugador.Posicion.PORTERO, "Porteros"),
]


def inicio(request):
    resumen = Jugador.objects.aggregate(
        total=Count("id"),
        edad_prom=Avg("edad"),
        altura_prom=Avg("altura_cm"),
        peso_prom=Avg("peso_kg"),
    )
    # Alineación: jugadores agrupados por posición (delanteros arriba, portero abajo)
    jugadores = Jugador.objects.order_by("dorsal")
    lineas = [
        (etiqueta, [j for j in jugadores if j.posicion == valor])
        for valor, etiqueta in ORDEN_LINEAS
    ]
    # Distribución por pierna buena
    total = resumen["total"] or 0
    piernas = []
    for valor, etiqueta in Jugador.Pierna.choices:
        cantidad = Jugador.objects.filter(pierna_buena=valor).count()
        porcentaje = round(cantidad * 100 / total) if total else 0
        piernas.append({"etiqueta": etiqueta, "cantidad": cantidad, "porcentaje": porcentaje})
    contexto = {"resumen": resumen, "lineas": lineas, "piernas": piernas}
    return render(request, "jugadoresapp/inicio.html", contexto)


ORDENES = {
    "nombre": ("apellido", "nombre"),
    "dorsal": ("dorsal",),
    "edad": ("edad", "apellido"),
    "altura": ("-altura_cm", "apellido"),
    "peso": ("-peso_kg", "apellido"),
}


def lista(request):  # READ (listado + búsqueda + filtros + orden + paginación)
    jugadores = Jugador.objects.all()
    q = request.GET.get("q", "").strip()
    posicion = request.GET.get("posicion", "")
    pierna = request.GET.get("pierna", "")
    orden = request.GET.get("orden", "nombre")
    if orden not in ORDENES:
        orden = "nombre"
    if q:
        jugadores = jugadores.filter(
            Q(nombre__icontains=q) | Q(apellido__icontains=q)
        )
    if posicion in Jugador.Posicion.values:
        jugadores = jugadores.filter(posicion=posicion)
    else:
        posicion = ""
    if pierna in Jugador.Pierna.values:
        jugadores = jugadores.filter(pierna_buena=pierna)
    else:
        pierna = ""
    jugadores = jugadores.order_by(*ORDENES[orden])

    pagina = Paginator(jugadores, 10).get_page(request.GET.get("page"))
    params = request.GET.copy()
    params.pop("page", None)
    contexto = {
        "pagina": pagina,
        "q": q,
        "posicion": posicion,
        "pierna": pierna,
        "orden": orden,
        "ordenes": [("nombre", "Apellido"), ("dorsal", "Dorsal"), ("edad", "Edad"),
                    ("altura", "Altura"), ("peso", "Peso")],
        "posiciones": Jugador.Posicion.choices,
        "piernas": Jugador.Pierna.choices,
        "querystring": params.urlencode(),
    }
    return render(request, "jugadoresapp/lista.html", contexto)


def detalle(request, pk):  # READ (un registro)
    jugador = get_object_or_404(Jugador, pk=pk)
    return render(request, "jugadoresapp/detalle.html", {"jugador": jugador})


def crear(request):  # CREATE
    if request.method == "POST":
        form = JugadorCrearForm(request.POST)
        if form.is_valid():
            jugador = form.save()
            messages.success(request, f"Jugador {jugador.nombre_completo} creado.")
            return redirect("jugadoresapp:lista")
    else:
        form = JugadorCrearForm()
    return render(request, "jugadoresapp/crear.html", {"form": form})


def editar(request, pk):  # UPDATE
    jugador = get_object_or_404(Jugador, pk=pk)
    if request.method == "POST":
        form = JugadorEditarForm(request.POST, instance=jugador)
        if form.is_valid():
            form.save()
            messages.success(request, f"Jugador {jugador.nombre_completo} actualizado correctamente.")
            return redirect("jugadoresapp:lista")
    else:
        form = JugadorEditarForm(instance=jugador)
    return render(request, "jugadoresapp/editar.html", {"form": form, "jugador": jugador})


def eliminar(request, pk):  # DELETE (con confirmación)
    jugador = get_object_or_404(Jugador, pk=pk)
    if request.method == "POST":
        nombre = jugador.nombre_completo
        jugador.delete()
        messages.success(request, f"Jugador {nombre} eliminado correctamente.")
        return redirect("jugadoresapp:lista")
    return render(request, "jugadoresapp/eliminar.html", {"jugador": jugador})
