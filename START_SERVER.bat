@echo off
REM Script de démarrage du serveur Django avec PostgreSQL
echo ========================================
echo DEMARRAGE DU SERVEUR DJANGO
echo Base de donnees: PostgreSQL
echo ========================================
echo.

REM Activation de l'environnement virtuel
echo [1/3] Activation de l'environnement virtuel...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo Erreur: Impossible d'activer l'environnement virtuel
    echo Assurez-vous que .venv existe
    pause
    exit /b 1
)

REM Verification des migrations
echo [2/3] Verification des migrations...
python manage.py migrate --check
if errorlevel 1 (
    echo.
    echo Des migrations sont necessaires. Execution...
    python manage.py migrate
)

REM Démarrage du serveur
echo [3/3] Demarrage du serveur Django...
echo.
echo ========================================
echo SERVEUR PRET !
echo ========================================
echo Acces local: http://127.0.0.1:8000
echo Acces reseau: http://0.0.0.0:8000
echo ========================================
echo.
echo Appuyez sur CTRL+C pour arreter le serveur
echo.

python manage.py runserver 0.0.0.0:8000
