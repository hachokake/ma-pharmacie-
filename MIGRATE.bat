@echo off
REM Script pour exécuter les migrations sur PostgreSQL
echo ========================================
echo MIGRATION VERS POSTGRESQL
echo ========================================
echo.

REM Activation de l'environnement virtuel
echo [1/2] Activation de l'environnement virtuel...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo Erreur: Impossible d'activer l'environnement virtuel
    echo Assurez-vous que .venv existe
    pause
    exit /b 1
)

echo [2/2] Execution des migrations...
python manage.py migrate
if errorlevel 1 (
    echo.
    echo ========================================
    echo ERREUR LORS DE LA MIGRATION
    echo ========================================
    pause
    exit /b 1
)

echo.
echo ========================================
echo MIGRATION REUSSIE !
echo ========================================
pause
