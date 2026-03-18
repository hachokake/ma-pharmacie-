@echo off
REM ============================================
REM OUVRIR LE PROJET DANS ANDROID STUDIO
REM ============================================

echo.
echo ============================================
echo   OUVERTURE ANDROID STUDIO
echo ============================================
echo.

cd /d "%~dp0"

echo Synchronisation Capacitor...
call npx cap sync android

echo Ouverture d'Android Studio...
call npx cap open android

echo.
echo Android Studio va s'ouvrir dans quelques secondes...
echo.
echo Premiere ouverture = 2-5 min d'indexation
echo.
echo Dans Android Studio :
echo   1. Attendez la fin de l'indexation (barre en bas)
echo   2. Build ^> Build Bundle(s) / APK(s) ^> Build APK(s)
echo   3. Ou cliquez sur Run (fleche verte) pour tester
echo.
pause
