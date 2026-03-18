@echo off
REM ============================================
REM MISE À JOUR RAPIDE APK
REM Recompile et réinstalle automatiquement
REM ============================================

echo.
echo ============================================
echo   MISE A JOUR APK PHARMACARE
echo ============================================
echo.

cd /d "%~dp0"

echo [1/4] Copie des fichiers...
copy /Y "..\..\pharmacy\static\manifest.json" "www\" >nul 2>&1
copy /Y "..\..\pharmacy\static\service-worker.js" "www\" >nul 2>&1
xcopy /Y /E "..\..\pharmacy\static\icons\*" "www\icons\" >nul 2>&1

echo [2/4] Synchronisation...
call npx cap sync android >nul 2>&1

echo [3/4] Compilation...
cd android
call gradlew assembleDebug >nul 2>&1
cd ..

echo [4/4] Installation sur telephone...
set APK_PATH=android\app\build\outputs\apk\debug\app-debug.apk

adb devices
echo.
echo Installation de la mise a jour...
adb install -r "%APK_PATH%"

if errorlevel 1 (
    echo.
    echo ERREUR: Impossible d'installer
    echo.
    echo Verifiez que :
    echo   1. Le telephone est connecte en USB
    echo   2. Le debogage USB est active
    echo   3. ADB est installe
    echo.
    echo Sinon, transferez manuellement : %APK_PATH%
    start explorer "%CD%\android\app\build\outputs\apk\debug"
) else (
    echo.
    echo ============================================
    echo   MISE A JOUR INSTALLEE !
    echo ============================================
    echo.
    echo L'application a ete mise a jour sur votre telephone.
    echo Ouvrez PharmaCare et testez le scanner !
)

echo.
pause
