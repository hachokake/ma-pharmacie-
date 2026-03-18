@echo off
REM ============================================
REM TEST COMPLET DU SCANNER MOBILE
REM ============================================

echo.
echo ============================================
echo   TEST SCANNER MOBILE - DIAGNOSTIC
echo ============================================
echo.

cd /d "%~dp0"

echo [ETAPE 1] Verification environnement...
echo.

REM Verifier si Django tourne
powershell -Command "$response = try { Invoke-WebRequest -Uri 'http://localhost:8000' -UseBasicParsing -TimeoutSec 2 } catch { $null }; if ($response) { Write-Host 'OK - Django tourne sur port 8000' -ForegroundColor Green } else { Write-Host 'ERREUR - Django ne repond pas' -ForegroundColor Red; Write-Host 'Lancez d''abord : python manage.py runserver 0.0.0.0:8000' -ForegroundColor Yellow }"

echo.
echo [ETAPE 2] Verification ngrok...
echo.

where ngrok >nul 2>&1
if errorlevel 1 (
    echo NGROK non installe
    echo.
    echo Voulez-vous l'installer maintenant ? (O/N)
    set /p INSTALL="> "
    if /i "!INSTALL!"=="O" (
        echo.
        echo Installation de ngrok...
        powershell -Command "Invoke-WebRequest -Uri 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip' -OutFile 'ngrok.zip'; Expand-Archive -Path 'ngrok.zip' -DestinationPath '.' -Force; Remove-Item 'ngrok.zip'"
        echo OK - ngrok installe !
    ) else (
        echo Installation annulee.
        echo.
        echo Vous pouvez aussi compiler l'APK Android :
        echo   cd AppBuild\android-app
        echo   .\COMPILER_APK.bat
        pause
        exit /b 0
    )
) else (
    echo OK - ngrok est installe
)

echo.
echo [ETAPE 3] Test de connexion...
echo.

REM Tester si le port 8000 est accessible
netstat -an | findstr ":8000" >nul
if errorlevel 1 (
    echo ATTENTION : Aucun service n'ecoute sur le port 8000
    echo.
    echo Ouvrez un autre terminal et lancez :
    echo   python manage.py runserver 0.0.0.0:8000
    echo.
    pause
)

echo.
echo ============================================
echo   LANCEMENT DU TUNNEL HTTPS
echo ============================================
echo.
echo Instructions :
echo.
echo 1. Un tunnel HTTPS va se creer
echo 2. Vous verrez une URL comme : https://xxxxx.ngrok-free.app
echo 3. COPIEZ cette URL
echo 4. Ouvrez-la sur votre TELEPHONE
echo 5. Cliquez sur "Visit Site" si demande
echo 6. Connectez-vous normalement
echo 7. Allez dans "Ajouter Medicament"
echo 8. Cliquez "Scanner"
echo 9. Autorisez la camera
echo 10. CA FONCTIONNE !
echo.
echo ============================================
echo.
pause

echo.
echo Demarrage de ngrok...
echo.

.\ngrok http 8000

pause
