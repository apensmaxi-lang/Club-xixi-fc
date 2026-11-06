from django.contrib.auth import get_user_model
from django.test import TestCase, Client

class AuthTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(username="prueba", password="ClavePrueba123!")

    def test_anonymous_cannot_access_or_modify(self):
        for url in ["/", "/jugadores/", "/jugadores/nuevo/", "/jugadores/1/", "/jugadores/1/editar/", "/jugadores/1/eliminar/"]:
            for method in [self.client.get, self.client.post]:
                response = method(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith("/login/?next="))

    def test_login_errors_success_and_logout(self):
        self.assertEqual(self.client.get("/login/").status_code, 200)
        self.assertContains(self.client.post("/login/", {"username":"prueba", "password":"incorrecta"}), "incorrectos")
        response = self.client.post("/login/", {"username":"prueba", "password":"ClavePrueba123!", "next":"https://example.com/"})
        self.assertRedirects(response, "/")
        self.assertEqual(self.client.get("/jugadores/").status_code, 200)
        self.assertEqual(self.client.get("/logout/").status_code, 405)
        self.assertRedirects(self.client.post("/logout/"), "/login/")
        self.assertEqual(self.client.get("/jugadores/").status_code, 302)

    def test_csrf_required(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post("/login/", {}).status_code, 403)
        client.force_login(get_user_model().objects.get(username="prueba"))
        self.assertEqual(client.post("/logout/", {}).status_code, 403)

    def test_api_login_and_token_revocation(self):
        import json
        response = self.client.post("/api/login/", json.dumps({"username":"prueba", "password":"ClavePrueba123!"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        token = response.json()["token"]
        self.assertEqual(response.json()["expires_in"], 3600)
        self.client.defaults["HTTP_AUTHORIZATION"] = "Bearer " + token
        self.assertEqual(self.client.post("/api/logout/").status_code, 204)
        self.assertEqual(self.client.post("/api/logout/").status_code, 401)

    def test_api_login_rejects_invalid_credentials(self):
        import json
        self.assertEqual(self.client.get("/api/login/").status_code, 405)
        self.assertEqual(self.client.post("/api/login/", {}).status_code, 415)
        for value in ["{", "[]", "{}"]:
            self.assertEqual(self.client.post("/api/login/", value, content_type="application/json").status_code, 400)
        payload = json.dumps({"username":"prueba", "password":"incorrecta"})
        self.assertEqual(self.client.post("/api/login/", payload, content_type="application/json").status_code, 401)
        user = get_user_model().objects.get(username="prueba")
        user.is_active = False; user.save()
        payload = json.dumps({"username":"prueba", "password":"ClavePrueba123!"})
        self.assertEqual(self.client.post("/api/login/", payload, content_type="application/json").status_code, 401)
