"""Contrato compartido: login futuro entrega emitir_token(usuario)."""
from functools import wraps
from django.contrib.sessions.backends.db import SessionStore
from django.core import signing
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.utils.crypto import constant_time_compare

SALT = "club.jugadores.api.v1"
TOKEN_SECONDS = 3600

def emitir_token(usuario):
    session = SessionStore()
    session["api_uid"] = usuario.pk
    session.set_expiry(TOKEN_SECONDS)
    session.save()
    return signing.dumps({"uid": usuario.pk, "auth": usuario.get_session_auth_hash(), "sid": session.session_key}, salt=SALT)


def revocar_token(request):
    SessionStore(session_key=request.api_session_key).delete()

def token_required(view):
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        header = request.headers.get("Authorization", "")
        try:
            scheme, token = header.split(" ", 1)
            if scheme.lower() != "bearer" or not token:
                raise ValueError()
            data = signing.loads(token, salt=SALT, max_age=TOKEN_SECONDS)
            user = get_user_model().objects.get(pk=data["uid"], is_active=True)
            if not constant_time_compare(data["auth"], user.get_session_auth_hash()):
                raise ValueError()
        except (ValueError, KeyError, TypeError, signing.BadSignature, get_user_model().DoesNotExist):
            response = JsonResponse({"error": "Token ausente, inválido o vencido."}, status=401)
            response["WWW-Authenticate"] = "Bearer"
            return response
        session = SessionStore(session_key=data.get("sid"))
        if session.get("api_uid") != user.pk:
            response = JsonResponse({"error": "Token revocado o vencido."}, status=401)
            response["WWW-Authenticate"] = "Bearer"
            return response
        request.api_session_key = data["sid"]
        request.user = user
        return view(request, *args, **kwargs)
    return wrapped
