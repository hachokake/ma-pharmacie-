@echo off
REM ============================================
REM COMPILATION APK PHARMACARE - VERSION HTTP
REM Caméra fonctionne SANS HTTPS ni ngrok !
REM ============================================

echo.
echo ============================================
echo     COMPILATION APK PHARMACARE
echo     Version HTTP + Scanner integre
echo ============================================
echo.

REM Aller dans le dossier android-app
cd /d "%~dp0"

echo [1/6] Verification des fichiers...
if not exist "www" (
    echo ERREUR: Dossier www manquant !
    echo Installez d'abord : npm install
    pause
    exit /b 1
)

echo [2/6] Copie des fichiers statiques...
copy /Y "..\..\pharmacy\static\manifest.json" "www\" >nul 2>&1
copy /Y "..\..\pharmacy\static\service-worker.js" "www\" >nul 2>&1
if not exist "www\icons" mkdir "www\icons"
xcopy /Y /E "..\..\pharmacy\static\icons\*" "www\icons\" >nul 2>&1
echo OK - Fichiers copies

echo [3/6] Nettoyage du cache Capacitor...
if exist "android\.gradle" (
    rmdir /s /q "android\.gradle" >nul 2>&1
)
if exist "android\app\build" (
    rmdir /s /q "android\app\build" >nul 2>&1
)
echo OK - Cache nettoye

echo [4/6] Synchronisation Capacitor...
call npx cap sync android
if errorlevel 1 (
    echo ERREUR lors de la synchronisation !
    pause
    exit /b 1
)

echo [5/6] Compilation APK debug...
cd android
call gradlew clean assembleDebug
if errorlevel 1 (
    echo ERREUR lors de la compilation !
    pause
    exit /b 1
)
cd ..

echo [6/6] Recherche de l'APK...
set APK_PATH=android\app\build\outputs\apk\debug\app-debug.apk
if exist "%APK_PATH%" (
    echo.
    echo ============================================
    echo     COMPILATION REUSSIE !
    echo ============================================
    echo.
    echo APK genere : %APK_PATH%
    echo Taille : 
    for %%A in ("%APK_PATH%") do echo %%~zA octets
    echo.
    echo MODIFICATIONS INCLUSES :
    echo   - Camera fonctionne en HTTP (pas besoin HTTPS)
    echo   - Auto-autorisation des permissions
    echo   - Scanner integre natif
    echo   - Connexion directe a 10.79.9.100:8000
    echo.
    echo INSTALLATION :
    echo   Option 1: adb install -r "%APK_PATH%"
    echo   Option 2: Transferer sur telephone et installer
    echo.
    echo UTILISATION :
    echo   1. Ouvrir PharmaCare
    echo   2. Autoriser camera (une seule fois)
    echo   3. Scanner fonctionne !
    echo   4. Pas besoin de ngrok ou autre lien !
    echo.
    start explorer "%CD%\android\app\build\outputs\apk\debug"
) else (
    echo ERREUR: APK non trouve !
    echo Verifiez les logs ci-dessus.
)

echo.
pause
