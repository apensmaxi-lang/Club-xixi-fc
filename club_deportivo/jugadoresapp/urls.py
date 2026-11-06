from django.contrib.auth import views as auth_views
from django.views.decorators.http import require_POST
from django.urls import path

from . import views, auth_views as club_auth

app_name = "jugadoresapp"

urlpatterns = [
    path("api/login/", club_auth.api_login, name="api-login"),
    path("api/logout/", club_auth.api_logout, name="api-logout"),
    path("login/", auth_views.LoginView.as_view(template_name="jugadoresapp/login.html", next_page="jugadoresapp:inicio"), name="login"),
    path("logout/", require_POST(auth_views.LogoutView.as_view(next_page="jugadoresapp:login")), name="logout"),
    path("", views.inicio, name="inicio"),
    path("jugadores/", views.lista, name="lista"),
    path("jugadores/nuevo/", views.crear, name="crear"),
    path("jugadores/<int:pk>/", views.detalle, name="detalle"),
    path("jugadores/<int:pk>/editar/", views.editar, name="editar"),
    path("jugadores/<int:pk>/eliminar/", views.eliminar, name="eliminar"),
]
