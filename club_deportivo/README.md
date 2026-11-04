# Club Xixi FC — Django y MariaDB de XAMPP

## Configuración comprobada
Python 3.12, Django 5.0.14 y Django REST Framework 3.15.2 según las instrucciones del profesor. Conector PyMySQL 1.2.3 y MariaDB 10.4.32 de XAMPP.
Base: `club_deportivo_db`, host `127.0.0.1`, puerto `3306`.
El backend se llama `django.db.backends.mysql` también cuando el servidor es MariaDB.
Django 5.0 admite MariaDB 10.4 directamente. Se retiraron los parches de versión y de INSERT RETURNING, y la alteración artificial de versión del conector. Las versiones se fijan para reproducir el entorno de la clase; no se presenta esta instalación como un despliegue público de producción.

## Preparar y ejecutar (PowerShell, desde la raíz del repositorio)
```powershell
py -3.12 -m venv venv
.\venv\Scripts\python.exe -m pip install -r club_deportivo\requirements.txt
.\venv\Scripts\python.exe club_deportivo\manage.py migrate
.\venv\Scripts\python.exe club_deportivo\manage.py runserver
```
Iniciar primero MariaDB en el panel XAMPP, donde el botón está rotulado MySQL.
Solo en una instalación nueva, crear la base con `club_deportivo/crear_bd.sql`. No borrar ni recrear una base con datos.
También se puede ejecutar `club_deportivo/iniciar.bat`: usa el entorno del repositorio y se detiene si las migraciones fallan. No carga jugadores demo ni genera migraciones automáticamente.
Variables opcionales: DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT. Se leen del entorno; no se carga automáticamente un archivo .env.
La clave de firma se genera una vez en `club_deportivo/.secret-key`, excluida de Git. No compartirla. Se puede sustituir con DJANGO_SECRET_KEY. Cambiarla invalida las sesiones y tokens existentes.

## API
Rutas: GET/POST `/api/jugadores/`; GET/PUT/DELETE `/api/jugadores/ID/`.
Enviar `Authorization: Bearer TOKEN` y para POST/PUT `Content-Type: application/json`.
El endpoint que entrega el token se incorpora con la rama de login, entregada aparte. Django REST Framework queda instalado y registrado según las instrucciones; los endpoints actuales se implementan con vistas Django y tokens firmados propios, no con JWT ni TokenAuthentication de DRF.
PUT requiere todos los campos del jugador. Los errores de validación se devuelven en JSON.

## Pruebas
```powershell
.\venv\Scripts\python.exe club_deportivo\manage.py test jugadoresapp.tests_api
```
Django crea una base de pruebas separada; el usuario necesita permiso para crearla. Nunca configurar TEST.NAME igual a la base real.
Tras integrar login: añadir `jugadoresapp.tests_auth` al comando.
Para crear usuarios tras las migraciones: `python manage.py createsuperuser` desde club_deportivo y con el entorno activo.

## Git y colaboración
API: rama login/apirest. Login: rama feature/login en la copia del compañero.
Acordar primero una base común con estos ajustes de configuración y la migración inicial.
La API cambia jugadores/urls.py; el login cambia jugadoresapp/urls.py, views.py y base.html.
api_auth.py se comparte idéntico en ambas entregas. Coordinar sus modificaciones.
No subir venv, .secret-key, contraseñas ni bases SQLite. Revisar `git diff` y `git status` antes de cada commit.
