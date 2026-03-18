@echo off
chcp 65001 >nul
echo ================================================
echo   RÉINITIALISATION DES COMPTES UTILISATEURS
echo ================================================
echo.
echo Ce script va supprimer TOUS les comptes utilisateurs
echo et administrateurs de la base de données.
echo.
pause

python reset_users.py

echo.
echo ================================================
pause
