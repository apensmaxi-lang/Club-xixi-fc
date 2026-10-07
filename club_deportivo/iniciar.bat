@echo off
REM Requisitos: XAMPP con MySQL iniciado y la base creada (crear_bd.sql).
cd /d "%~dp0"

if not exist venv (
    echo Creando entorno virtual...
    python -m venv venv
)
call venv\Scripts\activate

echo Instalando dependencias...
pip install -r requirements.txt

echo Creando tablas en MySQL...
python manage.py makemigrations jugadoresapp
python manage.py migrate

echo Cargando jugadores de ejemplo (opcional, no duplica)...
python manage.py cargar_demo

echo Abriendo el servidor en http://127.0.0.1:8000/
python manage.py runserver
pause
