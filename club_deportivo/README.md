# Xixi FC

Proyecto de la EVA03 para administrar los jugadores del club. Permite agregar, consultar, editar y eliminar jugadores desde la página y desde una API.

## Cómo ejecutarlo

Necesitas Python 3.12 y XAMPP. Inicia MySQL en XAMPP y crea la base `club_deportivo_db`. Puedes usar el archivo `club_deportivo/crear_bd.sql` si aún no la tienes.

Desde la carpeta principal del proyecto:

```cmd
py -3.12 -m venv venv
venv\Scripts\python.exe -m pip install -r club_deportivo\requirements.txt
venv\Scripts\python.exe club_deportivo\manage.py migrate
venv\Scripts\python.exe club_deportivo\manage.py runserver
```

Abre [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## API de jugadores

| Método | Ruta | Función |
| --- | --- | --- |
| GET | `/api/jugadores/` | Listar jugadores |
| GET | `/api/jugadores/ID/` | Consultar un jugador |
| POST | `/api/jugadores/` | Agregar un jugador |
| PUT | `/api/jugadores/ID/` | Editar un jugador |
| DELETE | `/api/jugadores/ID/` | Eliminar un jugador |

Reemplaza `ID` por el número del jugador. La API responde en JSON y necesita el encabezado `Authorization: Bearer TOKEN`.

Para crear o editar, envía los datos en JSON con `Content-Type: application/json`. PUT requiere todos los campos del jugador. Se validan los datos y no se permiten dorsales repetidos.

El login que entrega el token se integra desde la rama del compañero. En esta rama puedes comprobar la API con las pruebas automáticas.

## Pruebas

```cmd
venv\Scripts\python.exe club_deportivo\manage.py test jugadoresapp.tests_api
```

Usan una base temporal para probar las operaciones y los errores sin modificar los jugadores guardados.
