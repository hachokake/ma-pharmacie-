@echo off
REM ============================================
REM ACTIVER HTTPS POUR SCANNER MOBILE
REM ============================================

echo.
echo ============================================
echo   ACTIVATION HTTPS POUR TELEPHONE
echo ============================================
echo.

cd /d "%~dp0"

REM Verifier si ngrok est installe
where ngrok >nul 2>&1
if errorlevel 1 (
    echo NGROK non trouve !
    echo.
    echo INSTALLATION AUTOMATIQUE...
    echo.
    
    REM Telecharger ngrok
    echo [1/3] Telechargement de ngrok...
    powershell -Command "Invoke-WebRequest -Uri 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip' -OutFile 'ngrok.zip'"
    
    echo [2/3] Extraction...
    powershell -Command "Expand-Archive -Path 'ngrok.zip' -DestinationPath '.' -Force"
    
    echo [3/3] Nettoyage...
    del ngrok.zip
    
    echo.
    echo OK - ngrok installe !
    echo.
)

echo ============================================
echo   DEMARRAGE DU TUNNEL HTTPS
echo ============================================
echo.
echo Le serveur Django doit etre deja lance sur le port 8000
echo.
echo Verifiez que Django tourne sur : http://localhost:8000
echo Si ce n'est pas le cas, ouvrez un autre terminal et lancez :
echo   python manage.py runserver 0.0.0.0:8000
echo.
pause

echo.
echo Demarrage du tunnel HTTPS...
echo.
echo ============================================
echo   VOUS ALLEZ RECEVOIR UNE URL HTTPS
echo ============================================
echo.
echo 1. Notez l'URL qui commence par https://....ngrok-free.app
echo 2. Ouvrez cette URL sur votre telephone
echo 3. Le scanner camera va fonctionner !
echo.
echo ============================================
echo.

REM Lancer ngrok
ngrok http 8000

pause
