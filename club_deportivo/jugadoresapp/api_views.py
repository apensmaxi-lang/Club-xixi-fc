import json
from django.db import IntegrityError, transaction
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .api_auth import token_required
from .forms import JugadorCrearForm, JugadorEditarForm, CAMPOS
from .models import Jugador


def serializar(jugador):
    data = {campo: getattr(jugador, campo) for campo in CAMPOS}
    data["id"] = jugador.pk
    data["peso_kg"] = str(jugador.peso_kg)
    return data


def metodo_no_permitido(allowed):
    response = JsonResponse({"error": "Método no permitido."}, status=405)
    response["Allow"] = allowed
    return response


def guardar(request, instance=None):
    if request.content_type != "application/json":
        return JsonResponse({"error": "Envía Content-Type: application/json."}, status=415)
    try:
        data = json.loads(request.body)
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"error": "JSON inválido."}, status=400)
    if not isinstance(data, dict):
        return JsonResponse({"error": "Se requiere un objeto JSON."}, status=400)
    if set(data) - set(CAMPOS):
        return JsonResponse({"error": "Hay campos desconocidos."}, status=400)
    if any(isinstance(value, (bool, list, dict)) for value in data.values()):
        return JsonResponse({"error": "Tipos de datos inválidos."}, status=400)
    form = JugadorEditarForm(data, instance=instance) if instance else JugadorCrearForm(data)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors.get_json_data()}, status=400)
    try:
        with transaction.atomic():
            jugador = form.save()
    except IntegrityError:
        return JsonResponse({"error": "El dorsal ya está en uso."}, status=400)
    response = JsonResponse(serializar(jugador), status=200 if instance else 201)
    if instance is None:
        response["Location"] = f"/api/jugadores/{jugador.pk}/"
    return response


# Solo se aceptan tokens explícitos, nunca cookies de sesión en estos endpoints.
@csrf_exempt
@token_required
def jugadores(request):
    if request.method == "GET":
        return JsonResponse([serializar(j) for j in Jugador.objects.all()], safe=False)
    if request.method == "POST":
        return guardar(request)
    return metodo_no_permitido("GET, POST")


@csrf_exempt
@token_required
def jugador(request, pk):
    if request.method not in ("GET", "PUT", "DELETE"):
        return metodo_no_permitido("GET, PUT, DELETE")
    try:
        item = Jugador.objects.get(pk=pk)
    except Jugador.DoesNotExist:
        return JsonResponse({"error": "Jugador no encontrado."}, status=404)
    if request.method == "GET":
        return JsonResponse(serializar(item))
    if request.method == "PUT":
        return guardar(request, instance=item)
    item.delete()
    return HttpResponse(status=204)
