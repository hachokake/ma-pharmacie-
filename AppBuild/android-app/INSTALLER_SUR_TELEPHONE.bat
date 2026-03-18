@echo off
REM ============================================
REM TEST ET INSTALLATION RAPIDE SUR TELEPHONE
REM ============================================

echo.
echo ============================================
echo   TEST APK SUR TELEPHONE
echo ============================================
echo.

cd /d "%~dp0"

set APK_PATH=android\app\build\outputs\apk\debug\app-debug.apk

REM Verifier si l'APK existe
if not exist "%APK_PATH%" (
    echo APK non trouve !
    echo Compilez d'abord avec COMPILER_APK.bat
    echo.
    pause
    exit /b 1
)

echo APK trouve : %APK_PATH%
echo.

REM Verifier si ADB est disponible
adb version >nul 2>&1
if errorlevel 1 (
    echo ADB non trouve !
    echo.
    echo Installez Android SDK Platform Tools :
    echo https://developer.android.com/studio/releases/platform-tools
    echo.
    echo Ou transferez manuellement l'APK sur votre telephone.
    echo.
    start explorer "%CD%\android\app\build\outputs\apk\debug"
    pause
    exit /b 1
)

echo ADB detecte !
echo.

REM Verifier si un telephone est connecte
adb devices
echo.

echo Voulez-vous installer sur le telephone connecte ? (O/N)
set /p CONFIRM="> "

if /i "%CONFIRM%"=="O" (
    echo.
    echo Installation en cours...
    adb install -r "%APK_PATH%"
    if errorlevel 1 (
        echo.
        echo ERREUR lors de l'installation !
        echo Verifiez que le debogage USB est active.
    ) else (
        echo.
        echo ============================================
        echo     INSTALLATION REUSSIE !
        echo ============================================
        echo.
        echo L'application PharmaCare est maintenant
        echo installee sur votre telephone.
        echo.
        echo Lancez-la et testez le scanner !
        echo Au premier lancement, autorisez la camera.
    )
) else (
    echo Installation annulee.
    echo.
    start explorer "%CD%\android\app\build\outputs\apk\debug"
)

echo.
pause
