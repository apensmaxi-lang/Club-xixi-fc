import json
from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from .api_auth import emitir_token, token_required, revocar_token, TOKEN_SECONDS


def method_error():
    response = JsonResponse({"error": "Método no permitido."}, status=405)
    response["Allow"] = "POST"
    return response


@never_cache
@csrf_exempt
@sensitive_post_parameters("password")
def api_login(request):
    if request.method != "POST":
        return method_error()
    if request.content_type != "application/json":
        return JsonResponse({"error": "Se requiere application/json."}, status=415)
    try:
        data = json.loads(request.body)
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"error": "JSON inválido."}, status=400)
    if not isinstance(data, dict):
        return JsonResponse({"error": "Se requiere un objeto JSON."}, status=400)
    username, password = data.get("username"), data.get("password")
    if not isinstance(username, str) or not isinstance(password, str) or not username.strip() or not password:
        return JsonResponse({"error": "Usuario y contraseña son obligatorios."}, status=400)
    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({"error": "Credenciales incorrectas."}, status=401)
    return JsonResponse({"token": emitir_token(user), "token_type": "Bearer", "expires_in": TOKEN_SECONDS})


@never_cache
@csrf_exempt
@token_required
def api_logout(request):
    if request.method != "POST":
        return method_error()
    revocar_token(request)
    return HttpResponse(status=204)
