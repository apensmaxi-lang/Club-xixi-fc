@echo off
setlocal
cd /d "%~dp0"
set "PROJECT_PYTHON=%~dp0..\venv\Scripts\python.exe"
if not exist "%PROJECT_PYTHON%" (
    echo Falta el entorno virtual. Consulta README.md para crearlo.
    exit /b 1
)
echo Verificando MariaDB de XAMPP y migraciones...
"%PROJECT_PYTHON%" manage.py migrate
if errorlevel 1 (
    echo Revisa que MariaDB este iniciado en XAMPP y que exista club_deportivo_db.
    exit /b 1
)
"%PROJECT_PYTHON%" manage.py runserver
endlocal
