# Club Deportivo — Gestión de Jugadores (Django + MySQL/MariaDB)

CRUD de jugadores con estos datos: **nombre, apellido, dorsal, edad, altura (cm), peso (kg), posición y pierna buena**.

## Abrir en Visual Studio Code
`Archivo > Abrir carpeta…` y elige la carpeta `club_deportivo` (la que contiene `manage.py`).
Abre la terminal integrada (`Ctrl + ñ`) y sigue los pasos de abajo. También puedes ejecutar con F5 ("Django: runserver").

## Conectar con XAMPP (MySQL)
La conexión ya está configurada en `jugadores/settings.py` con los valores por defecto de XAMPP:
base `club_deportivo`, usuario `root`, sin contraseña, host `127.0.0.1`, puerto `3306`.

1. Abre el **XAMPP Control Panel** y pulsa **Start** en **MySQL** (Apache no es necesario, solo si quieres abrir phpMyAdmin).
2. Abre http://localhost/phpmyadmin → pestaña **SQL** → pega el contenido de `crear_bd.sql` → **Continuar**
   (o pestaña **Importar** y eliges el archivo). Debe aparecer la base `club_deportivo` en la izquierda.
3. Abre la carpeta del proyecto en VS Code. En la terminal ejecuta `iniciar.bat`
   (crea el entorno virtual, instala dependencias, crea las tablas, carga datos de ejemplo y arranca el servidor).
4. Entra a http://127.0.0.1:8000/
5. Para ver los datos: phpMyAdmin → `club_deportivo` → tabla `jugadoresapp_jugador` → **Examinar**.

### Manual (sin el .bat)
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations jugadoresapp
python manage.py migrate
python manage.py cargar_demo      # opcional
python manage.py runserver
```

### Problemas frecuentes
- **Can't connect to MySQL server**: MySQL no está iniciado en XAMPP, o usa otro puerto (míralo en el Control Panel; si es 3307, cambia `DB_PORT` en settings.py).
- **Access denied for user 'root'**: tu MySQL tiene contraseña; ponla en `PASSWORD` de settings.py.
- **Unknown database 'club_deportivo'**: falta ejecutar `crear_bd.sql`.
- **MariaDB 10.5 or later is required**: XAMPP antiguo. Actualiza XAMPP o usa `pip install "Django==4.2.*"` (Python ≤ 3.12).
- Sin XAMPP, para probar: `set USE_SQLITE=1` antes de migrar.

> Si antes tenías una versión anterior con la tabla `jugadores_jugador`, bórrala (o borra y recrea la base) y elimina cualquier migración antigua dentro de `jugadoresapp/migrations/` (deja solo `__init__.py`).

## Estructura
Mismo esquema que el repo de referencia: un proyecto y una app con `manage.py`, `requirements.txt` y `.gitignore` en la raíz.
- `jugadores/` proyecto Django (settings.py con la conexión a la BD, urls.py raíz, wsgi.py).
- `jugadoresapp/` app: `models.py` (modelo `Jugador`), `forms.py` (crear/editar), `views.py` (CRUD), `urls.py`, `admin.py`.
- `jugadoresapp/templates/jugadoresapp/` base, inicio, lista, detalle, crear, editar, eliminar.

## CRUD
| Acción | Ruta |
|---|---|
| Listar / buscar / filtrar / ordenar | `/jugadores/` |
| Crear | `/jugadores/nuevo/` |
| Ver detalle | `/jugadores/<id>/` |
| Editar | `/jugadores/<id>/editar/` |
| Eliminar (con confirmación por POST) | `/jugadores/<id>/eliminar/` |

## Validaciones
Todos los campos son obligatorios · nombre y apellido solo letras · dorsal 1–99 y único · edad 5–60 · altura 100–230 cm · peso 20–150 kg (admite un decimal) · posición y pierna buena (derecha / izquierda / ambidiestro) se eligen de una lista.

## Ver el CRUD en la base de datos
phpMyAdmin → `club_deportivo` → tabla `jugadoresapp_jugador`; refresca tras cada acción en la web.
