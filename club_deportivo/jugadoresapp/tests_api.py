import json
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core import signing
from .api_auth import emitir_token, SALT
from .models import Jugador

class ApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="api", password="Prueba123!")
        self.token = emitir_token(self.user)
        self.client.defaults["HTTP_AUTHORIZATION"] = "Bearer " + self.token
        self.data = dict(nombre="Juan", apellido="Perez", dorsal=10, edad=24, altura_cm=180, peso_kg="75.5", posicion="DEFENSA", pierna_buena="DERECHA")

    def create(self, data=None):
        return self.client.post("/api/jugadores/", data=json.dumps(self.data if data is None else data), content_type="application/json")

    def test_crud_and_web_share_data(self):
        response = self.create()
        self.assertEqual(response.status_code, 201)
        url = response["Location"]
        self.assertEqual(self.client.get(url).json()["nombre"], "Juan")
        self.assertEqual(len(self.client.get("/api/jugadores/").json()), 1)
        self.client.force_login(self.user)
        self.assertContains(self.client.get("/jugadores/"), "Juan")
        data = dict(self.data, edad=30)
        self.assertEqual(self.client.put(url, json.dumps(data), content_type="application/json").status_code, 200)
        self.assertEqual(Jugador.objects.get().edad, 30)
        self.assertEqual(self.client.delete(url).status_code, 204)
        self.assertFalse(Jugador.objects.exists())
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_invalid_data_and_methods(self):
        for data in [{}, [], dict(self.data, edad=200), dict(self.data, nombre="123"), dict(self.data, dorsal=True)]:
            self.assertEqual(self.create(data).status_code, 400)
        self.assertEqual(self.create().status_code, 201)
        self.assertEqual(self.create().status_code, 400)
        url = "/api/jugadores/%s/" % Jugador.objects.get().pk
        self.assertEqual(self.client.put(url, "{}", content_type="application/json").status_code, 400)
        self.assertEqual(self.client.post("/api/jugadores/", "{", content_type="application/json").status_code, 400)
        self.assertEqual(self.client.post("/api/jugadores/", {}).status_code, 415)
        self.assertEqual(self.client.patch(url).status_code, 405)
        self.assertEqual(self.client.delete("/api/jugadores/9999/").status_code, 404)

    def test_tokens(self):
        for token in ["", "Bearer falso", "Basic abc"]:
            self.client.defaults["HTTP_AUTHORIZATION"] = token
            self.assertEqual(self.client.get("/api/jugadores/").status_code, 401)
            self.assertEqual(self.create().status_code, 401)
        self.client.defaults["HTTP_AUTHORIZATION"] = "Bearer " + self.token
        with patch("django.core.signing.time.time", return_value=1):
            expired = emitir_token(self.user)
        self.client.defaults["HTTP_AUTHORIZATION"] = "Bearer " + expired
        self.assertEqual(self.client.get("/api/jugadores/").status_code, 401)
        self.client.defaults["HTTP_AUTHORIZATION"] = "Bearer " + self.token
        self.user.set_password("OtraClave123!"); self.user.save()
        self.assertEqual(self.client.get("/api/jugadores/").status_code, 401)
